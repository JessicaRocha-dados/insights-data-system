# Visão Geral do Projeto InsightOS

### 1.1 Introdução

#### Resumo Executivo
[cite_start]Este documento detalha o ciclo de vida completo do projeto InsightOS, uma iniciativa para transformar dados brutos de utilizadores em inteligência de negócio acionável[cite: 3]. [cite_start]O desafio central era a ineficiência na aquisição de clientes da plataforma SaaS InsightOS, que não conseguia distinguir leads de alto e baixo potencial[cite: 4, 1169].

[cite_start]A solução foi a construção de um sistema de dados de ponta a ponta, centrado num modelo de machine learning de Lead Scoring e complementado por uma análise de Lifetime Value (LTV)[cite: 5, 1170]. [cite_start]O sistema rastreia a jornada do utilizador, calcula uma pontuação de probabilidade de conversão e, por fim, automatiza esse processo[cite: 5, 1171].

[cite_start]O resultado é um sistema robusto que permite à InsightOS identificar os leads de maior potencial, otimizar os investimentos em marketing e tomar decisões de produto baseadas em dados, transformando a organização de uma empresa reativa para uma proativa e orientada por dados[cite: 6, 1186]. [cite_start]Os resultados financeiros validam a abordagem: a análise de LTV provou que leads da campanha `google_gestao_agil` geram um retorno 2,3 vezes (ou 130%) superior ao de outros canais, fornecendo uma recomendação de investimento inequívoca [cite: 75, 88-89, 1146-1147].

#### Objetivos Estratégicos
O objetivo principal era resolver a "cegueira estratégica" na aquisição de clientes. As metas de negócio incluíam:
* [cite_start]**Priorização de Vendas:** Permitir que a equipa de vendas priorize esforços nos leads de maior potencial [cite: 87, 1187-1188].
* **Otimização de ROI:** Conectar o investimento em marketing (CAC) com a receita gerada (LTV), fornecendo uma base matemática para a alocação de orçamento.
* [cite_start]**Inteligência de Produto:** Identificar os pontos de maior atrito na jornada do utilizador para priorizar melhorias no produto [cite: 91-92].

#### Objetivos Técnicos
Para alcançar os objetivos estratégicos, as seguintes metas técnicas foram estabelecidas:
* Construir um pipeline de dados de ponta a ponta, desde a captura de eventos no navegador até o armazenamento persistente.
* Implementar um modelo de *Lead Scoring* para prever a probabilidade de conversão.
* Desenvolver modelos de LTV (BG/NBD e Gamma-Gamma) para quantificar o valor financeiro por segmento de cliente.
* [cite_start]Automatizar o processo de pontuação de novos leads num ambiente de produção na nuvem [cite: 78-79, 1204].

#### Justificativa das Tecnologias
A arquitetura foi construída sobre uma pilha de tecnologias moderna, escalável e de código aberto.
* [cite_start]**FastAPI:** Escolhido para a API de ingestão devido à sua alta performance assíncrona e validação de dados nativa com Pydantic[cite: 12, 13, 1196, 1198].
* [cite_start]**PostgreSQL (via Supabase):** Selecionado como um banco de dados relacional robusto e gerenciado na nuvem[cite: 14, 1199].
* [cite_start]**Render:** Utilizado para a implantação da API e do Cron Job de automação[cite: 36, 81, 1204].
* [cite_start]**Metabase (via Docker):** Implementado como a ferramenta de BI para visualização, por ser uma solução de código aberto e eficiente para rodar localmente[cite: 41, 1203].
* **Scikit-learn / Lifetimes:** Bibliotecas padrão da indústria para modelagem de machine learning e LTV, respetivamente.