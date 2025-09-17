import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAções DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Análise de ROI & LTV")
PAGE_COLOR = "#28a745"  # Verde Sucesso

# --- CONTEÚDO DA PÁGINA ---
st.markdown(
    f"<h1 style='text-align: center; color: {PAGE_COLOR};'>💰 Análise de ROI e Lifetime Value (LTV)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6c757d;'>Conectando todos os insights ao valor financeiro para a tomada de decisão final.</h3>", unsafe_allow_html=True)

# --- DADOS E GRÁFICO ---
ltv_data = {'campanha': ['google_gestao_agil', 'outra_campanha_1', 'outra_campanha_2',
                         'outra_campanha_3'], 'Valor do Cliente (LTV)': [73.60, 33.71, 32.46, 30.38]}
df_ltv = pd.DataFrame(ltv_data)
cac_data = {'campanha': ['google_gestao_agil', 'outra_campanha_1', 'outra_campanha_2',
                         'outra_campanha_3'], 'Custo de Aquisição (CAC)': [25.50, 15.20, 14.80, 16.10]}
df_cac = pd.DataFrame(cac_data)
df_final = pd.merge(df_ltv, df_cac, on='campanha')

df_melted = df_final.melt(id_vars='campanha', value_vars=[
                          'Valor do Cliente (LTV)', 'Custo de Aquisição (CAC)'], var_name='metrica', value_name='valor')

fig = px.bar(
    df_melted, x='campanha', y='valor', color='metrica', barmode='group',
    text_auto='.2f', title='LTV vs. CAC por Campanha (Horizonte de 12 meses)',
    # Verde e Vermelho
    color_discrete_map={
        'Valor do Cliente (LTV)': PAGE_COLOR, 'Custo de Aquisição (CAC)': '#dc3545'}
)
fig.update_traces(textposition='outside')
# --- MUDANÇA ABAIXO ---
fig.update_layout(title_x=0.5, yaxis_title="Valor em Reais (R$)", xaxis_title=None, plot_bgcolor='white',
                  legend_title_text=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# --- CONCLUSÃO ESTRATÉGICA APROFUNDADA ---
st.markdown(f"""
<style>
.conclusion-box {{
    background-color: rgba(40, 167, 69, 0.1);
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
    <h3>Conclusão Estratégica: A Decisão Baseada em Dados</h3>
    <p>A análise financeira é o clímax do projeto, quantificando o valor das nossas descobertas. Os dados são inequívocos: o LTV médio de um cliente da campanha <strong>'google_gestao_agil'</strong> é de <strong>R$ 73,60</strong>.</p>
    <p>Este valor é aproximadamente <strong>2.3 vezes maior</strong> que o LTV médio das outras campanhas. Em termos de negócio, isto significa que o retorno sobre o investimento desta campanha é massivamente superior, justificando um custo de aquisição mais elevado.</p>
    <p><strong>Recomendação Final:</strong> A InsightOS deve <strong>realocar o orçamento de marketing de forma agressiva para escalar a campanha 'google_gestao_agil'</strong>. Cada cliente adquirido através desta fonte tem um valor projetado que é mais do que o dobro dos outros canais, garantindo o caminho mais rápido e seguro para um crescimento lucrativo e sustentável.</p>
</div>
""", unsafe_allow_html=True)
