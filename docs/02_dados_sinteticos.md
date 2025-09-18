# 3. Geração de Dados Sintéticos

### 3.1 Justificativa

A geração de dados sintéticos foi uma decisão estratégica na fase inicial do projeto. A principal justificativa foi a necessidade de um **ambiente de laboratório controlado**. Em vez de lidar com dados do mundo real, que poderiam ser escassos ou "ruidosos", a simulação nos permitiu:
1.  **Validar o Pipeline:** Garantir que o pipeline de ponta a ponta (coleta, API, BD, BI) funcionava corretamente.
2.  **Criar Padrões Fortes:** Injetar intencionalmente padrões e correlações realistas nos dados (ex: `google_gestao_agil` convertendo mais).
3.  **Testar Modelos:** Criar um "quebra-cabeças" com uma solução conhecida para validar se nossos modelos de ML e LTV eram capazes de "encontrar" os padrões que criamos.

### 3.2 Implementação
O processo foi implementado no notebook `01_data_simulation.ipynb`, utilizando `pandas` para a criação e manipulação dos DataFrames e `faker` para gerar dados falsos com aparência real (nomes, emails).

**1. Simulação do Funil de Conversão (Lead Scoring):**
A estratégia central foi um funil probabilístico. Em vez de eventos aleatórios, a ocorrência de eventos-chave era uma cascata de decisões com probabilidades condicionais.

**Lógica de Transição (Exemplo `project_created`):**
* Um **usuário** só poderia criar um projeto se já tivesse verificado o e-mail.
* A probabilidade de criar um projeto era **condicional** à campanha de origem.
* Isso foi implementado para simular que certas campanhas atraem **usuários** mais qualificados.

O código-fonte abaixo ilustra essa lógica:

```python
# Lógica da simulação do funil
# A probabilidade de criar um projeto depende da campanha

prob_create_project = 0.55 if user['acquisition_campaign'] == 'google_gestao_agil' else 0.30

# O evento só ocorre se a condição probabilística for satisfeita

if random.random() < prob_create_project:
    # Gera o evento 'project_created'
    events.append(...) 
    
    # Lógica aninhada para a próxima etapa do funil (assinatura)
    prob_subscribe = 0.40 if user['acquisition_campaign'] == 'google_gestao_agil' else 0.15
    if random.random() < prob_subscribe:
        events.append(...)
        # Atualiza o status do usuário no DataFrame original
        users_df.loc[users_df['user_id'] == user_id, 'status'] = 'converted'

        
### 3.3 Simulação de Transações (LTV):
Para a análise de LTV, um segundo script gerou um log de transações. De forma similar, os dados foram intencionalmente enviesados para que clientes da google_gestao_agil tivessem:

Maior probabilidade de recompra.

Ciclo de compra mais curto.

Ticket médio (valor monetário) superior.

###  Avaliação da Qualidade e Desafios:

A "qualidade" dos dados foi validada pela capacidade de inseri-los e analisá-los. Durante a inserção, desafios técnicos reais foram superados:

duplicate key value... "users_pkey": Resolvido limpando as tabelas antes de cada inserção para garantir um ambiente de teste limpo.

uplicate key value... "users_email_key": Resolvido adicionando uma lógica de verificação para garantir que a biblioteca faker não gerasse e-mails duplicados.

Out of range float values...: Resolvido convertendo valores np.nan (do pandas) para None (Python nativo), que é compatível com o formato JSON null do banco de dados.

A validação final foi visual, usando o Metabase (Figura 2) para gerar um gráfico de funil, que confirmou que a lógica probabilística foi capturada e armazenada corretamente.