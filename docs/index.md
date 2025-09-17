# Visão Geral do Projeto InsightOS

> **Nota:** Esta é a documentação técnica completa. Para o sumário executivo visual e os dashboards de resultados finais para gestores (construídos em Streamlit), por favor visite o nosso **[Hub Estratégico de Insights (no Notion)](https://www.notion.so/Projeto-InsightOS-Hub-Estrat-gico-de-Resultados-2713b90412c580bea009e48c7d2a8483?source=copy_link)**.

### 1.1 Introdução

#### Resumo Executivo
Este documento detalha o ciclo de vida completo do projeto InsightOS, uma iniciativa para transformar dados brutos de utilizadores em inteligência de negócio acionável. O desafio central era a ineficiência na aquisição de clientes da plataforma SaaS InsightOS, que não conseguia distinguir leads de alto e baixo potencial.

A solução foi a construção de um sistema de dados de ponta a ponta, centrado num modelo de machine learning de Lead Scoring e complementado por uma análise de Lifetime Value (LTV). O sistema rastreia a jornada do utilizador, calcula uma pontuação de probabilidade de conversão e, por fim, automatiza esse processo.

O resultado é um sistema robusto que permite à InsightOS identificar os leads de maior potencial, otimizar os investimentos em marketing e tomar decisões de produto baseadas em dados, transformando a organização de uma empresa reativa para uma proativa e orientada por dados. Os resultados financeiros validam a abordagem: a análise de LTV provou que leads da campanha `google_gestao_agil` geram um retorno 2,3 vezes (ou 130%) superior ao de outros canais, fornecendo uma recomendação de investimento inequívoca.

#### Objetivos Estratégicos
O objetivo principal era resolver a "cegueira estratégica" na aquisição de clientes. As metas de negócio incluíam:
* **Priorização de Vendas:** Permitir que a equipa de vendas priorize esforços nos leads de maior potencial 
* **Otimização de ROI:** Conectar o investimento em marketing (CAC) com a receita gerada (LTV), fornecendo uma base matemática para a alocação de orçamento.
* **Inteligência de Produto:** Identificar os pontos de maior atrito na jornada do utilizador para priorizar melhorias no produto.

#### Objetivos Técnicos
Para alcançar os objetivos estratégicos, as seguintes metas técnicas foram estabelecidas:
* Construir um pipeline de dados de ponta a ponta, desde a captura de eventos no navegador até o armazenamento persistente.
* Implementar um modelo de *Lead Scoring* para prever a probabilidade de conversão.
* Desenvolver modelos de LTV (BG/NBD e Gamma-Gamma) para quantificar o valor financeiro por segmento de cliente.
* Automatizar o processo de pontuação de novos leads num ambiente de produção na nuvem.

#### Justificativa das Tecnologias
A arquitetura foi construída sobre uma pilha de tecnologias moderna, escalável e de código aberto.
* **FastAPI:** Escolhido para a API de ingestão devido à sua alta performance assíncrona e validação de dados nativa com Pydantic.
* **PostgreSQL (via Supabase):** Selecionado como um banco de dados relacional robusto e gerenciado na nuvem.
* **Render:** Utilizado para a implantação da API e do Cron Job de automação.
* **Metabase (via Docker):** Implementado como a ferramenta de BI para visualização, por ser uma solução de código aberto e eficiente para rodar localmente.
* **Scikit-learn / Lifetimes:** Bibliotecas padrão da indústria para modelagem de machine learning e LTV, respetivamente.