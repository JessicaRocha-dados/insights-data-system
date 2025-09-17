# 2. Arquitetura do Sistema

### 2.1 Pipeline de Dados
O sistema é um pipeline de dados de ponta a ponta que transforma cliques anónimos em inteligência de negócio. O fluxo é o seguinte:

1.  **Coleta (Navegador):** O `tracker.js` no site captura eventos (ex: `page_view`) e dados de atribuição (UTMs)[cite: 1195, 1079].Ele gera um `visitor_id` único e armazena dados de *first/last touch* no `localStorage`.
2.  **Ingestão (API FastAPI):** Os dados são enviados via `POST` para a API (main.py) hospedada no Render.
3.  **Validação:** A API usa modelos Pydantic para validar rigorosamente se o *payload* do evento corresponde ao schema definido, rejeitando dados malformados.
4.  **Armazenamento (PostgreSQL):** Dados validados são inseridos de forma segura no banco de dados PostgreSQL (Supabase).
5.  **Análise e Modelagem (Python/Jupyter):** Scripts Python e notebooks conectam-se ao banco de dados para realizar engenharia de atributos (feature engineering) e treinar os modelos de ML (Lead Scoring e LTV).
6.  **Automação (Cron Job):** Um script `score_updater.py` é executado diariamente pelo Render. Ele carrega o modelo treinado, busca novos utilizadores, calcula seus scores e atualiza o banco de dados.
7. **Visualização (Metabase):** O Metabase, rodando localmente via Docker, conecta-se ao banco de dados (em modo de leitura) para criar dashboards e relatórios.

### 2.2 Tecnologias Utilizadas

| Categoria | Tecnologia | Justificativa (Conforme Documentação de Planejamento) |
| :--- | :--- | :--- |
| **Coleta** | JavaScript (custom) | Script `tracker.js` para captura de eventos de front-end e atribuição |
| **Ingestão (API)** | Python / FastAPI | API assíncrona para validação (Pydantic) e persistência de dados. |
| **Armazenamento** | PostgreSQL (Supabase) | Banco de dados relacional gerenciado na nuvem, servindo como repositório central. |
| **Análise/Modelagem**| Python / Jupyter |Scripts e Notebooks para engenharia de atributos e treinamento de modelos. |
| **Automação** | Cron Job (Render) | Executa o script `score_updater.py` diariamente para pontuar novos leads. |
| **Visualização** | Metabase (via Docker) | Ferramenta de BI open-source rodando localmente para análise visual. |

### 2.3 Diagrama do Sistema
[cite_start]O diagrama a seguir ilustra o fluxo de dados completo do sistema InsightOS.

**Figura 1 - Diagrama de Fluxo de Dados do Sistema InsightOS**
![Diagrama de Fluxo de Dados do Sistema InsightOS](img/arquitetura_fluxo.png)

 *Fonte: Documentação de Planejamento.docx 