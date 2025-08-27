# ===========================================================================
# API DE TRACKING DE EVENTOS PARA O PROJETO INSIGHTOS
# ===========================================================================
#
# Autor: Jessica Rocha
# Data: 27 de Agosto de 2025
#
# Objetivo:
# Esta API, construída com FastAPI, serve como o ponto de entrada para todos
# os dados de tracking recolhidos no front-end. A sua principal
# responsabilidade é receber os eventos, validar a sua estrutura e
# inseri-los de forma segura no nosso banco de dados PostgreSQL no Supabase.
#
# ===========================================================================

# --- 0. IMPORTAÇÕES E CONFIGURAÇÃO INICIAL ---

# Começo por importar todas as ferramentas necessárias.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field # Pydantic é crucial para validar os dados que chegam.
from typing import Optional, Dict, Any # Para definir os tipos de dados dos nossos modelos.
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware # Para permitir que o nosso site (front-end) comunique com esta API.
from sqlalchemy import create_engine, text # SQLAlchemy é a biblioteca que uso para comunicar com o banco de dados PostgreSQL.
import json # Para converter objetos Python em formato JSON antes de os guardar no banco.
import os # Para ler as variáveis de ambiente de forma segura.
from dotenv import load_dotenv # Para carregar as variáveis de ambiente de um ficheiro .env localmente.

# Carrega as variáveis de ambiente (como a DATABASE_URL) do ficheiro .env.
# Isto é uma boa prática para não expor senhas diretamente no código.
load_dotenv()

# --- 1. CONEXÃO COM O BANCO DE DADOS ---

# Obtenho a string de conexão do banco de dados a partir das variáveis de ambiente.
# No Render, esta variável é configurada diretamente no painel do serviço.
DATABASE_URL = "postgresql://postgres.oteqjiqifwhmqdjblmyl:oGIrVVuxJ826fXDP@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"

# Verifico se a DATABASE_URL foi realmente carregada. Se não, o programa para com um erro claro.
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida.")

# Crio a "engine", que é o objeto do SQLAlchemy que gere a conexão com o banco de dados.
# O bloco try/except garante que, se a conexão falhar no arranque, eu fico a saber imediatamente.
try:
    engine = create_engine(DATABASE_URL)
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")
    engine = None


# --- 2. DEFINIÇÃO DOS MODELOS DE DADOS (SCHEMAS) ---

# Usando o Pydantic, defino a estrutura exata dos dados que espero receber.
# Se o front-end enviar algo diferente, a API irá rejeitar automaticamente com um erro claro.

class Attribution(BaseModel):
    """ Define a estrutura dos parâmetros de atribuição de marketing (UTMs, etc.). """
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    gclid: Optional[str] = None
    fbclid: Optional[str] = None

class AttributionData(BaseModel):
    """ Agrupa os dados de atribuição de primeiro e último toque. """
    first_touch: Optional[Attribution] = None
    last_touch: Optional[Attribution] = None

class EventPayload(BaseModel):
    """ Este é o modelo principal. Define a estrutura de cada evento que a API recebe. """
    event_type: str
    visitor_id: str
    timestamp: datetime
    url: str
    page_title: str
    event_properties: Dict[str, Any] = Field(default_factory=dict) # Um dicionário flexível para dados extras.
    attribution: AttributionData


# --- 3. INICIALIZAÇÃO E CONFIGURAÇÃO DA APLICAÇÃO FASTAPI ---

# Crio a instância principal da minha aplicação FastAPI.
app = FastAPI(
    title="InsightOS Tracking API",
    description="API para coletar eventos de tracking do front-end.",
    version="1.0.0"
)

# Configuro o CORS (Cross-Origin Resource Sharing).
# Isto é uma medida de segurança do navegador. Basicamente, estou a dizer ao navegador
# para permitir que o meu site (ex: localhost:5500) possa enviar pedidos para esta API.
origins = [
    "http://localhost", "http://localhost:5500",
    "http://127.0.0.1", "http://127.0.0.1:5500",
    "null" # Permite testes locais a partir de ficheiros HTML abertos diretamente.
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.).
    allow_headers=["*"], # Permite todos os cabeçalhos.
)


# --- 4. DEFINIÇÃO DOS ENDPOINTS (ROTAS) DA API ---

@app.get("/")
def read_root():
    """ Crio um endpoint raiz (a página inicial da API) apenas para verificar se ela está online. """
    return {"message": "API da InsightOS está online e conectada ao banco de dados."}


@app.post("/event")
def track_event(payload: EventPayload):
    """
    Este é o endpoint principal. Ele "ouve" por pedidos POST na rota /event.
    Quando um evento chega, ele é validado contra o modelo EventPayload e, se for válido,
    é inserido no banco de dados.
    """
    # Verifico se a conexão com o banco de dados foi estabelecida no arranque.
    if engine is None:
        raise HTTPException(status_code=500, detail="A conexão com o banco de dados não foi estabelecida.")

    # Converte o objeto Pydantic recebido num dicionário Python normal para ser mais fácil de manipular.
    event_data = payload.model_dump()

    # Preparo a minha query SQL. Uso a função text() e placeholders (:key) do SQLAlchemy
    # para me proteger contra ataques de SQL Injection.
    query = text("""
        INSERT INTO user_events (visitor_id, event_type, "timestamp", url, page_title, event_properties, first_touch, last_touch)
        VALUES (:visitor_id, :event_type, :timestamp, :url, :page_title, :event_properties, :first_touch, :last_touch)
    """)

    # Preparo os parâmetros que serão inseridos na query.
    # Os campos JSON (event_properties, etc.) precisam de ser convertidos para texto (string) antes de serem inseridos.
    params = {
        "visitor_id": event_data["visitor_id"],
        "event_type": event_data["event_type"],
        "timestamp": event_data["timestamp"],
        "url": event_data["url"],
        "page_title": event_data["page_title"],
        "event_properties": json.dumps(event_data["event_properties"]),
        "first_touch": json.dumps(event_data["attribution"]["first_touch"]),
        "last_touch": json.dumps(event_data["attribution"]["last_touch"]),
    }

    # Executo a inserção no banco de dados.
    try:
        # O 'with engine.connect() as connection:' é uma forma segura de garantir que a conexão
        # é aberta e fechada corretamente, mesmo que ocorra um erro.
        with engine.connect() as connection:
            connection.execute(query, params)
            connection.commit() # Confirmo a transação para que os dados sejam salvos permanentemente.
        
        # Se tudo correu bem, imprimo uma mensagem de sucesso no log do servidor.
        print(f"Evento '{payload.event_type}' salvo no banco de dados para o visitor_id: {payload.visitor_id}")
        # E envio uma resposta de sucesso de volta para o front-end.
        return {"status": "success", "message": "Evento salvo com sucesso!"}

    except Exception as e:
        # Se ocorrer qualquer erro durante a inserção, capturo-o.
        print(f"Erro ao salvar evento no banco de dados: {e}")
        # E levanto uma exceção HTTP, que envia uma mensagem de erro clara para o front-end.
        raise HTTPException(status_code=500, detail="Erro ao salvar evento no banco de dados.")
