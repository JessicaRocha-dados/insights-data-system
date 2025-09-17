import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Análise de Funil")
PAGE_COLOR = "#6a0dad"  # Roxo/Púrpura

# --- CONTEÚDO DA PÁGINA ---
st.markdown(f"<h1 style='text-align: center; color: {PAGE_COLOR};'>🔻 Análise do Funil de Conversão</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6c757d;'>Diagnosticando a saúde da jornada do cliente e os pontos de atrito.</h3>", unsafe_allow_html=True)

# --- DADOS E GRÁFICO ---
etapas = ['Trial Signup', 'User Verified', 'Project Created', 'Subscription Started']
valores = [406, 388, 161, 45]

fig = go.Figure(go.Funnel(
    y = etapas,
    x = valores,
    textposition = "inside",
    textinfo = "value+percent initial",
    opacity = 1.0, marker = {"color": ["#480ca8", "#560bad", "#7209b7", "#b5179e"],
    "line": {"width": 2, "color": "white"}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
)
fig.update_layout(title="Funil de Conversão - Da Inscrição à Assinatura", title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

# --- CONCLUSÃO ESTRATÉGICA APROFUNDADA ---
st.markdown(f"""
<style>
.conclusion-box {{
    background-color: rgba(106, 13, 173, 0.1);
    border-left: 5px solid {PAGE_COLOR};
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-top: 2rem;
}}
.conclusion-box h3 {{
    color: {PAGE_COLOR};
    margin-top: 0;
}}
</style>
<div class="conclusion-box">
    <h3>Conclusão Estratégica: O Ponto de Atrito Crítico</h3>
    <p>A análise do funil revela de forma inequívoca o maior "buraco no balde" da InsightOS. Enquanto a passagem de <strong>Trial Signup</strong> para <strong>User Verified</strong> tem uma retenção altíssima de 95.6%, a taxa de conversão para a etapa seguinte, <strong>Project Created</strong>, despenca para apenas 41.5%.</p>
    <p><strong>Implicação para o Negócio:</strong> Estamos a perder mais de metade dos nossos utilizadores engajados e verificados no momento em que deveriam experimentar o valor central do nosso produto. Este é o ponto de maior alavancagem para o crescimento.</p>
    <p><strong>Recomendação:</strong> A equipe produto deve priorizar a investigação desta etapa. As perguntas a serem respondidas são: O que está a impedir os utilizadores de criar o seu primeiro projeto? O processo é muito complexo? Faltam instruções claras? O valor não é evidente? Uma melhoria, mesmo que pequena, nesta taxa de conversão terá um efeito cascata em todo o funil, aumentando significativamente o número de clientes pagantes.</p>
</div>
""", unsafe_allow_html=True)