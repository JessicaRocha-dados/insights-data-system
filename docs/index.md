# Visão Geral do Projeto InsightOS

> **Nota:** Esta é a documentação técnica completa. Para o sumário executivo visual e os dashboards de resultados finais para gestores (construídos em Streamlit), por favor visite o nosso **[Hub Estratégico de Insights (no Notion)](https://www.notion.so/Projeto-InsightOS-Hub-Estrat-gico-de-Resultados-2713b90412c580bea009e48c7d2a8483?source=copy_link)**.

> **1.1 Introdução**

>* Resumo Executivo

Este documento detalha o ciclo de vida completo do projeto InsightOS, uma iniciativa destinada a transformar dados brutos de usuários em inteligência de negócios acionável. O principal desafio identificado foi a ineficiência na aquisição de clientes pela plataforma SaaS InsightOS, que não era capaz de diferenciar leads de alto potencial daqueles com baixo potencial.

A solução desenvolvida consistiu em um sistema de processamento de dados de ponta a ponta, centrado em um modelo de machine learning para Lead Scoring e complementado por uma análise detalhada de Lifetime Value (LTV). O sistema é capaz de acompanhar a jornada dos usuários, calcular uma pontuação representando a probabilidade de conversão e, ao final, automatizar esse processo, garantindo eficiência operacional.

O sistema permite à InsightOS identificar leads com maior potencial de conversão, otimizar os investimentos em marketing e tomar decisões estratégicas de produto com base em dados. Essa abordagem transformou a organização, que passou de reativa para proativa e orientada por dados. Os resultados financeiros validaram a solução: a análise de Lifetime Value demonstrou que leads originados da campanha google_gestao_agil geram um retorno 2,3 vezes maior (ou 130% superior) em comparação com outros canais, fornecendo uma recomendação clara para priorizar investimentos nesse segmento.

># Objetivos Estratégicos 

O principal objetivo do projeto foi superar a chamada "cegueira estratégica" na aquisição de clientes. Para isso, definiram-se as seguintes metas de negócios:

**Priorização de Vendas:** Capacitar a equipe comercial a direcionar seus esforços para leads com maior potencial de conversão, maximizando a eficiência nas operações de vendas.

**Otimização do ROI:** Relacionar o investimento em marketing, medido pelo Custo de Aquisição de Clientes (CAC), à receita gerada, representada pelo Lifetime Value (LTV), fornecendo uma base quantitativa para a alocação estratégica de orçamento.

**Inteligência de Produto:** Mapear os principais pontos de atrito na jornada dos usuários para identificar oportunidades de melhoria e promover aprimoramentos estratégicos no produto.

># Objetivos Técnicos

Para que os objetivos estratégicos fossem alcançados, foram definidas as seguintes metas técnicas:

1. Construir um pipeline completo de dados, desde a captura de eventos no navegador até o armazenamento seguro e persistente em banco de dados.

2. Implementar um modelo de Lead Scoring para prever a probabilidade de conversão de leads.

3. Desenvolver modelos de Lifetime Value (LTV), com base nas metodologias BG/NBD e Gamma-Gamma, para mensurar o valor financeiro de cada segmento de cliente.

4. Automatizar o processo de cálculo e pontuação de novos leads em um ambiente de produção na nuvem.

># Justificativa das Tecnologias

A arquitetura do sistema foi projetada com uma pilha de tecnologias moderna, escalável e baseada em soluções de código aberto. A escolha das ferramentas priorizou alta performance, flexibilidade e confiabilidade:

**FastAPI:** Utilizada para a criação da API de ingestão de dados, destacando-se por sua elevada performance simultânea e validação de dados nativa através da integração com Pydantic.

**PostgreSQL (via Supabase):** Adotado pela sua robustez, confiabilidade e capacidade de gerenciamento eficiente na nuvem.

**Render:** Escolhido para implantação da API e para o gerenciamento do Cron Job de automação.

**Metabase (via Docker):** Utilizado como ferramenta de Business Intelligence (BI) para visualização de dados, sendo uma solução eficiente, flexível e de código aberto que pode ser executada localmente.

**Scikit-learn / Lifetimes:** Bibliotecas amplamente reconhecidas no mercado. Enquanto a Scikit-learn foi usada para machine learning, a Lifetimes contribuiu para análise probabilística de Lifetime Value, garantindo precisão nas análises.

# Modelo Preditivo de Lead Scoring
Esta fase focou em estruturar os dados brutos para que fossem compreensíveis para um modelo de machine learning, com o objetivo de prever a probabilidade de conversão de leads.

>#    Engenharia de Atributos

O trabalho principal consistiu na criação de uma tabela única (feature_table), cuja cada linha representava um usuário e cada coluna, uma característica descritiva. Destaque para:

1. O log de eventos foi consolidado por meio de pivot_table, transformando ações em contagens numéricas (e.g., events_project_created).

2. Informações de marketing, como a campanha de origem, foram extraídas de campos JSON.

3. A variável-alvo (target_converted) foi criada a partir da coluna de status, convertendo-a em valores binários (0 para "não convertido", 1 para "convertido").

>#    Análise Exploratória de Dados (EDA)

A análise da feature_table forneceu importantes aprendizados:

**Dados Desequilibrados**: Apenas 10,1% dos usuários eram convertidos, indicando forte desequilíbrio que exigiria estratégias específicas durante a modelagem.

**Impacto de Campanha:** A campanha google_gestao_agil apresentou taxas de conversão significativamente maiores, validando a hipótese inicial.

**Multicolinearidade:** Identificou-se forte correlação (0,96) e alto Fator de Inflação da Variância (VIF > 25) entre as variáveis events_trial_signup e events_user_verified, exigindo a remoção de uma delas para modelos sensíveis.

>#    Modelagem e Avaliação

Foram treinados dois modelos e ambos integrados em um pipeline com as seguintes características:

Pré-processamento: Incluiu a padronização de variáveis numéricas, codificação de categorias e configuração de pesos balanceados (class_weight='balanced') devido ao desequilíbrio nos dados.

>#    Modelos utilizados:

**Regressão Logística (v1):** Modelo simples, eficiente e interpretável.

**XGBoost (v2):** Modelo avançado, com maior capacidade de aprendizado para dados complexos.

># Resultado e Decisão Estratégica

**Performance:** Ambos os modelos apresentaram 100% em todas as métricas (AUC, precisão e recall) devido à clareza dos padrões nos dados sintéticos.

**Decisão Final:** Optou-se pela Regressão Logística, priorizando interpretabilidade, baixo custo computacional e robustez contra sobreajustes (overfitting).

>#    Análise de Impacto Financeiro (Lifetime Value - LTV)

Esta última etapa visou quantificar financeiramente o impacto das descobertas anteriores.

>**Metodologia**

Foi criado um novo dataset sintético de transações, no qual os clientes da campanha google_gestao_agil tinham maior frequência de compra e valores médios elevados. Dois modelos padrão foram utilizados:

BG/NBD: Para prever frequência e probabilidade de churn.

Gamma-Gamma: Para prever o valor médio das transações.

>##   Resultado Final
O LTV médio dos clientes da campanha google_gestao_agil foi 2,3 vezes maior ($73,60) do que o das campanhas regulares ($32). Essa análise forneceu η base matemática para priorizar investimentos nesta campanha.