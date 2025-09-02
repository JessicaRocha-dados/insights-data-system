# ==============================================================================
# SCRIPT DE ATUALIZAÇÃO DE LEAD SCORE (score_updater.py)
# ==============================================================================
# Autora: Jessica Rocha, Cientista de Dados
# Data: 02 de setembro de 2025
#
# ---
# MEU RACIOCÍNIO (Jéssica):
# Este script representa a passagem do nosso projeto do mundo da análise para o
# mundo da produção. O meu objetivo aqui não é explorar, mas sim executar de
# forma eficiente e robusta uma tarefa repetitiva: pontuar novos leads.
#
# Estruturei o código para ser:
#   - Robusto: Com tratamento de erros em cada etapa crítica.
#   - Eficiente: Buscando apenas os dados estritamente necessários.
#   - Legível: Com uma função `main` que orquestra o processo passo a passo.
#
# Este é o motor que irá alimentar a equipa de vendas da InsightOS com
# inteligência de dados, todos os dias.
# ==============================================================================

import os
import pandas as pd
import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv, find_dotenv
import joblib
import json
from datetime import datetime

def connect_to_supabase():
    """
    Estabelece a conexão com o Supabase de forma segura, carregando as
    credenciais do ficheiro .env. Retorna um objeto de cliente ou None se falhar.
    """
    try:
        # Uso find_dotenv() para garantir que o ficheiro .env seja encontrado,
        # independentemente de onde o script for executado.
        load_dotenv(find_dotenv())
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("Credenciais do Supabase não encontradas no ficheiro .env.")
            
        print("Conexão com o Supabase estabelecida.")
        return create_client(url, key)
    except Exception as e:
        print(f"Erro crítico ao conectar com o Supabase: {e}")
        return None

def main():
    """
    Função principal que orquestra todo o processo de scoring.
    """
    print(f"\n--- [START] Iniciando script de atualização de Lead Score: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

    supabase = connect_to_supabase()
    if not supabase:
        return # Termina a execução se a conexão com o banco de dados falhar.

    # --- Passo 1: Carregar o Modelo ---
    # Minha primeira ação é carregar o modelo. Se o ficheiro não for encontrado
    # ou estiver corrompido, não faz sentido continuar. É uma abordagem "fail-fast".
    try:
        pipeline_filename = "notebooks/lead_scoring_pipeline_v1.joblib"
        model_pipeline = joblib.load(pipeline_filename)
        print(f"Modelo '{pipeline_filename}' carregado com sucesso.")
    except Exception as e:
        print(f"Erro crítico ao carregar o modelo: {e}")
        return

    # --- Passo 2: Identificar Leads para Pontuar ---
    # Eu otimizo a minha consulta para buscar TODOS os utilizadores cujo `lead_score`
    # seja nulo. Isto dá-me a lista completa de trabalho a ser feito.
    try:
        response = supabase.table('users').select('user_id, visitor_id, plan, status').filter('lead_score', 'is', 'null').execute()
        all_users_to_score_df = pd.DataFrame(response.data)
        
        if all_users_to_score_df.empty:
            print("Nenhum utilizador novo para pontuar. Processo concluído.")
            return

        print(f"Encontrados {len(all_users_to_score_df)} utilizadores no total para pontuar.")
        
    except Exception as e:
        print(f"Erro ao buscar dados do banco: {e}")
        return

    # --- LÓGICA DE PROCESSAMENTO EM LOTES (BATCH PROCESSING) ---
    # Para evitar erros de "Request-URI Too Large", não vou processar todos os
    # utilizadores de uma vez. Vou "fatiar" o trabalho em lotes mais pequenos.
    batch_size = 100 # A minha decisão: processar 100 utilizadores de cada vez.
    total_users_to_score = len(all_users_to_score_df)
    
    for start in range(0, total_users_to_score, batch_size):
        end = start + batch_size
        user_batch_df = all_users_to_score_df.iloc[start:end]
        
        print(f"\n--- Processando Lote {start//batch_size + 1}/{(total_users_to_score + batch_size - 1)//batch_size} (utilizadores {start+1}-{min(end, total_users_to_score)}) ---")

        try:
            # --- Passo 3: Coletar Eventos PARA ESTE LOTE ---
            visitor_ids_to_fetch = user_batch_df['visitor_id'].tolist()
            response_events = supabase.table('user_events').select('*').in_('visitor_id', visitor_ids_to_fetch).execute()
            events_df = pd.DataFrame(response_events.data)
            print(f"Carregados {len(events_df)} eventos para este lote.")

            # --- Passo 4: Reconstruir a Feature Table PARA ESTE LOTE ---
            print("Iniciando a reconstrução da feature table para o lote...")
            if not events_df.empty:
                events_pivot = events_df.pivot_table(index='visitor_id', columns='event_type', aggfunc='size', fill_value=0).reset_index()
                events_pivot.columns = ['visitor_id'] + ['events_' + col for col in events_pivot.columns[1:]]
                signup_events = events_df[events_df['event_type'] == 'trial_signup'].copy()
                signup_events['campaign'] = signup_events['first_touch'].apply(lambda x: json.loads(x).get('campaign', 'unknown') if x and isinstance(x, str) else 'unknown')
                campaign_df = signup_events[['visitor_id', 'campaign']].drop_duplicates(subset=['visitor_id'])
                feature_table = pd.merge(user_batch_df, events_pivot, on='visitor_id', how='left')
                feature_table = pd.merge(feature_table, campaign_df, on='visitor_id', how='left')
                event_cols = [col for col in feature_table.columns if 'events_' in col]
                feature_table[event_cols] = feature_table[event_cols].fillna(0)
            else:
                feature_table = user_batch_df.copy()
                expected_event_cols = ['events_project_created', 'events_subscription_started', 'events_trial_signup', 'events_user_verified']
                for col in expected_event_cols:
                    feature_table[col] = 0
                feature_table['campaign'] = 'unknown'
            print("Feature table do lote reconstruída com sucesso.")

            # --- Passo 5: Calcular os Scores PARA ESTE LOTE ---
            print("Calculando os scores para o lote...")
            model_features = ['plan', 'events_project_created', 'events_subscription_started', 'events_trial_signup', 'events_user_verified', 'campaign']
            for col in model_features:
                if col not in feature_table.columns:
                    feature_table[col] = 0 if 'events_' in col else 'unknown'
            X_new = feature_table[model_features]
            scores = model_pipeline.predict_proba(X_new)[:, 1]
            feature_table['lead_score'] = scores
            print(f"Scores calculados para {len(feature_table)} utilizadores neste lote.")

            # --- Passo 6: Atualizar o Banco de Dados PARA ESTE LOTE ---
            print("Iniciando a atualização dos scores do lote no banco de dados...")
            updates_successful = 0
            for index, row in feature_table.iterrows():
                try:
                    user_id = row['user_id']
                    score = row['lead_score']
                    rounded_score = round(score, 4)
                    supabase.table('users').update({'lead_score': rounded_score}).eq('user_id', user_id).execute()
                    updates_successful += 1
                except Exception as e_update:
                    print(f"Aviso: Erro ao atualizar o user_id {user_id}: {e_update}")
            print(f"{updates_successful}/{len(feature_table)} utilizadores do lote atualizados com sucesso.")

        except Exception as e_batch:
            print(f"Erro crítico ao processar o lote {start//batch_size + 1}. A saltar para o próximo lote. Erro: {e_batch}")
            
    print(f"\n--- [END] Processo de atualização de Lead Score concluído: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

if __name__ == "__main__":
    main()