import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAções DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Qualidade por Campanha")
PAGE_COLOR = "#008080"  # Teal

# --- CONTEÚDO DA PÁGINA ---
st.markdown(f"<h1 style='text-align: center; color: {PAGE_COLOR};'>📊 Qualidade de Leads por Campanha de Marketing</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6c757d;'>Quais canais de marketing atraem os clientes mais valiosos?</h3>", unsafe_allow_html=True)

# --- DADOS E GRÁFICO ---
data = {
    'Campanha de Marketing': ['google_gestao_agil', 'unknown', 'organic', 'facebook_freelancer'],
    'Lead Score Médio': [0.245, 0.097, 0.067, 0.030]
}
df_quality = pd.DataFrame(data)

fig = px.bar(
    df_quality, x='Lead Score Médio', y='Campanha de Marketing', orientation='h',
    text_auto='.3f', title='Qualidade Média dos Leads por Origem',
    color_discrete_sequence=[PAGE_COLOR] * len(df_quality)
)
fig.update_layout(title_x=0.5, plot_bgcolor='white', yaxis={'categoryorder':'total ascending'}, xaxis_title="Lead Score Médio (Probabilidade de Conversão)")
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# --- CONCLUSÃO ESTRATÉGICA APROFUNDADA ---
st.markdown(f"""
<style>
.conclusion-box {{
    background-color: rgba(0, 128, 128, 0.1);
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
    <h3>Conclusão Estratégica: O Canal de Ouro</h3>
    <p>A análise é conclusiva: a campanha <strong>google_gestao_agil</strong> não é apenas a melhor, ela está numa categoria própria, com um Lead Score médio de <strong>0.245</strong>. Este valor é drasticamente superior a todas as outras fontes, que geram leads com scores médios tendendo a zero (entre 0.030 e 0.097).</p>
    <p><strong>Implicação para o Negócio:</strong> A InsightOS pode, pela primeira vez, medir a eficácia das suas campanhas não apenas pelo volume de leads, mas pela <strong>qualidade preditiva</strong> desses leads. Isto permite uma alocação de orçamento muito mais inteligente.</p>
    <p><strong>Recomendação:</strong> Realocar o orçamento de marketing para fortalecer e escalar a campanha <strong>google_gestao_agil</strong>. Ao investir mais no canal que comprovadamente atrai os clientes de maior potencial, a empresa pode esperar um aumento significativo no seu Retorno sobre o Investimento (ROI) e alinhar as equipes de Marketing e Vendas em torno de um objetivo comum: atrair leads de qualidade.</p>
</div>
""", unsafe_allow_html=True)