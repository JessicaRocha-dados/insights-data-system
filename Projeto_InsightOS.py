import streamlit as st
from datetime import datetime
import locale

# Configurando o locale para português para exibir o mês corretamente
try:
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Portugal.1252')


# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO GLOBAL
# ==============================================================================

st.set_page_config(
    page_title="Dashboard Estratégico - InsightOS",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. SOLUÇÃO DEFINITIVA: USANDO st.logo() PARA A MARCA NO TOPO
# Esta função coloca o logo ACIMA da navegação automática.
st.logo(
    "https://em-content.zobj.net/source/microsoft-teams/363/high-voltage_26a1.png",
    icon_image="https://em-content.zobj.net/source/microsoft-teams/363/high-voltage_26a1.png"
)


# Injeção de CSS para customização avançada do design
st.markdown("""
<style>
    /* Estilo geral */
    body {
        font-family: 'Sans Serif', sans-serif;
    }
    .main {
        background-color: #F8F9FA;
        padding: 2rem;
    }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
        padding: 1.5rem;
    }
    
    /* Container para o rodapé da sidebar */
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        width: 88%;
    }
    
    /* Caixa de "Análise por" */
    .analise-box {
        background-color: #F0F2F6; /* Cinza claro */
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem; /* Espaço entre as caixas do rodapé */
        text-align: left;
    }
    
    /* Caixa "Sobre os Dados" */
    .sobre-box {
        background-color: #FFF3E0; /* Laranja claro */
        border-radius: 0.5rem;
        padding: 1rem;
        font-size: 0.9rem;
    }
    .sobre-box strong {
        color: #E65100; /* Laranja escuro */
    }
    .sobre-box .icon {
        float: left;
        margin-right: 10px;
        font-size: 1.5rem;
    }
    
    /* Títulos */
    h1, h2 {
        color: #212529;
        font-weight: 600;
    }
    h3 {
        color: #495057;
        font-weight: 500;
    }
    
    /* Cards da página inicial */
    .card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card h3 {
        color: #0d6efd;
    }
    
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# BARRA LATERAL (SIDEBAR) - ESTRUTURA FINAL
# ==============================================================================
with st.sidebar:
    # A navegação automática do Streamlit aparecerá aqui, abaixo do logo.
    
    # INFORMAÇÕES SECUNDÁRIAS AGRUPADAS NO RODAPÉ
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    
    data_atual = datetime.now().strftime("%d de %B de %Y")
    st.markdown(f'<div class="analise-box">Análise por:<br><b>Jéssica Rocha</b><br>{data_atual}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sobre-box">
        <span class="icon">⚠️</span>
        <div>
            <strong>Sobre os Dados</strong><br>
            O LTV foi calculado com base nos modelos do notebook <code>03_ltv_analysis.ipynb</code> e o CAC é uma simulação estratégica.
            <br><br>
            <strong>Nota de Transparência:</strong> A análise de LTV utiliza o modelo Gamma-Gamma, que assume independência entre frequência e valor monetário. Descobrimos uma correlação fraca, violando essa premissa. Portanto, os valores de LTV devem ser vistos como um poderoso índice comparativo, e não uma previsão contábil exata.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# CONTEÚDO DA PÁGINA PRINCIPAL
# ==============================================================================

st.markdown("<h1 style='text-align: center;'>💡 Projeto InsightOS: Uma Jornada de Dados Estratégica</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6c757d;'>Conectando todos os insights ao valor financeiro para a tomada de decisão final.</h3>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("O Problema de Negócio")
    st.markdown("Um grande volume de novos leads estava a sobrecarregar a equipe de vendas, resultando em custos crescentes e perda de oportunidades. A questão era: “Como podemos usar os dados para transformar o ruído em sinal, permitindo que a equipe foque nos leads que realmente importam?”.")

with col2:
    st.subheader("A Arquiteta da Solução")
    st.markdown("Construí uma solução de ponta a ponta, desde a infraestrutura de captura de dados até a análise final de valor financeiro (LTV), para responder a essa questão.")

st.markdown("<br><hr><br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><h3>🔻 Funil de Conversão</h3><p>Identificação dos pontos de atrito na jornada do cliente para otimização do produto.</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><h3>📊 Qualidade de Leads</h3><p>Prova de que a campanha "google_gestao_agil" atrai os leads de maior valor preditivo.</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><h3>🧠 Lead Scoring</h3><p>Construção de um sistema de ML para priorizar leads, aumentando a eficiência da equipe de vendas.</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card"><h3>💰 Análise de ROI & LTV</h3><p>Tradução dos insights em valor financeiro, provando um retorno 2.3x maior na campanha certa.</p></div>', unsafe_allow_html=True)
