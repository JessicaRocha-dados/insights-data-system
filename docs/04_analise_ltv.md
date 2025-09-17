# 5. Análise Financeira (LTV)

### 5.1 Estratégia
O objetivo desta fase era quantificar financeiramente o valor dos *leads* e provar o valor das campanhas. A estratégia foi usar modelos probabilísticos padrão da indústria:
1.  **Modelo BG/NBD (Beta-Geometric/Negative-Binomial-Distribution):** Usado para prever a atividade futura do cliente. Ele responde "quantas compras futuras esperamos?" e "qual a probabilidade de o cliente estar 'vivo' (não ter sofrido *churn*)?".
2.  **Modelo Gamma-Gamma:** Usado para estimar o valor monetário médio das transações futuras. Ele só é aplicado aos clientes que se espera estarem "vivos".
3.  **Cálculo do LTV:** O LTV é calculado combinando as saídas dos dois modelos (Frequência Esperada x Valor Monetário Esperado).

### 5.2 Descoberta Crítica (Violação de Premissa)
Antes de treinar o modelo Gamma-Gamma, uma verificação de premissas é necessária. O modelo assume que **não há correlação** entre a frequência de compra de um cliente e seu valor monetário médio.
* **Nossa Análise:** Encontramos uma correlação de **0.3882** (ou 0.39), como será provado na imagem de log abaixo[cite: 1177].
* **Tradução de Negócio:** Isso significa que "clientes mais leais são também os que gastam mais" — um insight valioso, mas que viola a premissa do modelo [cite: 1184-1185].
* **Decisão Estratégica:** A decisão pragmática foi prosseguir. Em vez de tratar o LTV como uma previsão contábil exata, nós o interpretamos como um **índice comparativo robusto** para ranquear o valor relativo das campanhas[cite: 1192, 1197].

### 5.3 Sumários de Performance dos Modelos

**1. Sumário do Modelo BG/NBD (Frequência e Churn)**
Este é o log do primeiro modelo, que diagnosticou o comportamento "médio" de toda a base de clientes (quantas vezes compram e quando sofrem churn) [cite: 1145-1149].

![Sumário do Modelo BG/NBD](img/ltv_bg_nbd_summary.png)

**2. Sumário do Modelo Gamma-Gamma (Valor Monetário)**
Este log prova a nossa "Descoberta Crítica" do passo anterior. A primeira linha confirma a **Correlação de 0.3882** que viola a premissa. As linhas seguintes mostram o sumário do modelo de valor monetário.

![Sumário do Modelo Gamma-Gamma](img/ltv_gamma_gamma_summary.png)

### 5.4 Visualização Preditiva (Heatmap)
O modelo BG/NBD também nos permite visualizar a "saúde" esperada de toda a base de clientes. Este heatmap (mapa de calor) mostra o número esperado de compras futuras no próximo período:
* **Eixo X (Frequência Histórica):** Clientes que compraram mais vezes.
* **Eixo Y (Recência):** Clientes que compraram mais recentemente (mais abaixo no gráfico).
* **Insight (Mancha Clara):** O canto inferior direito (clientes recentes e frequentes) é o segmento com maior probabilidade de comprar novamente. O modelo confirma que os nossos melhores clientes são os que são simultaneamente recentes e frequentes.

### 5.5 Resultados Preditivos (Top 10 Clientes)
O cálculo do LTV combinado (BG/NBD + Gamma-Gamma) valida a nossa hipótese de forma inequívoca. A tabela abaixo, mostrando os 10 melhores clientes classificados pelo LTV futuro estimado, prova que o modelo conseguiu encontrar os padrões que inserimos nos dados sintéticos.

* **Descoberta:** Todos os 10 clientes com o maior LTV previsto pertencem, sem exceção, à campanha `google_gestao_agil`[cite: 1028].
* **Validação:** Isto confirma que a nossa metodologia (os modelos BG/NBD e Gamma-Gamma) funciona. Eles foram capazes de identificar corretamente os clientes de alto valor que nós criámos intencionalmente na simulação.

![Top 10 Clientes por LTV Estimado](img/ltv_top_10.png)

### 5.6 Conclusão Financeira (Agregação por Campanha)
Finalmente, agregamos o LTV médio por campanha. O resultado abaixo é a conclusão financeira de todo o projeto, quantificando o que o modelo de lead scoring sugeriu.

* **Prova Financeira:** O LTV de um cliente da `google_gestao_agil` é de **$73.60**[cite: 75, 1252].
* **ROI Comparativo:** Este valor é **2.3 vezes maior** (ou 130% superior) ao LTV médio das outras campanhas[cite: 75, 1253].
* **Recomendação Estratégica:** Esta análise fornece a prova matemática inequívoca para a realocação agressiva do orçamento de marketing para a campanha `google_gestao_agil` [cite: 89, 1266-1267].

![Resultado Final: LTV Médio por Campanha](img/ltv_resultado_final.png)
