# Importa as bibliotecas necessárias
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from sqlalchemy import create_engine, text
import json # Importa a biblioteca JSON padrão do Python

# --- 0. CONFIGURAÇÃO DO BANCO DE DADOS ---
# CORREÇÃO: A senha foi "URL-encoded". O caractere * foi substituído por %2A
# para evitar erros de interpretação na string de conexão.
DATABASE_URL = "postgresql://postgres.oteqjiqifwhmqdjblmyl:zEwvwco51h8pya7B@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"

# Cria a "engine" de conexão com o banco de dados
try:
    engine = create_engine(DATABASE_URL)
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")
    engine = None

# --- 1. Definição dos Modelos de Dados (Schemas) ---
class Attribution(BaseModel):
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    gclid: Optional[str] = None
    fbclid: Optional[str] = None

class AttributionData(BaseModel):
    first_touch: Optional[Attribution] = None
    last_touch: Optional[Attribution] = None

class EventPayload(BaseModel):
    event_type: str
    visitor_id: str
    timestamp: datetime
    url: str
    page_title: str
    event_properties: Dict[str, Any] = Field(default_factory=dict)
    attribution: AttributionData

# --- 2. Criação da Aplicação FastAPI ---
app = FastAPI(
    title="InsightOS Tracking API",
    description="API para coletar eventos de tracking do front-end.",
    version="1.0.0"
)

# --- CONFIGURAÇÃO DE CORS ---
origins = [
    "http://localhost", "http://localhost:5500",
    "http://127.0.0.1", "http://127.0.0.1:5500",
    "null"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Definição dos Endpoints da API ---

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"message": "API da InsightOS está online e conectada ao banco de dados."}

@app.post("/event")
def track_event(payload: EventPayload):
    """
    Recebe um evento de tracking e o salva no banco de dados.
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Conexão com o banco de dados não foi estabelecida.")

    # Converte o payload Pydantic para um dicionário Python
    event_data = payload.model_dump()

    # Prepara a query SQL para inserir os dados
    # Usamos `text()` para segurança contra SQL Injection e placeholders (:key)
    query = text("""
        INSERT INTO user_events (visitor_id, event_type, "timestamp", url, page_title, event_properties, first_touch, last_touch)
        VALUES (:visitor_id, :event_type, :timestamp, :url, :page_title, :event_properties, :first_touch, :last_touch)
    """)

    # Prepara os parâmetros para a query
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

    try:
        # Executa a query no banco de dados
        with engine.connect() as connection:
            connection.execute(query, params)
            connection.commit() # Confirma a transação
        
        print(f"Evento '{payload.event_type}' salvo no banco de dados para o visitor_id: {payload.visitor_id}")
        return {"status": "success", "message": "Evento salvo com sucesso!"}

    except Exception as e:
        print(f"Erro ao salvar evento no banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar evento no banco de dados.")