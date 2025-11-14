import pandas as pd
import numpy as np
import google.generativeai as genai
import mysql.connector
from mysql.connector import Error

# ------------------------------------------------------------------
# 1. CONFIGURAÇÃO (SEU CÓDIGO DE IA + CONFIG DE DB)
# ------------------------------------------------------------------

# Configure a API Key do Gemini (como no seu código)
# ATENÇÃO: Nunca deixe chaves de API visíveis em código de produção!
# Considere usar variáveis de ambiente.
genai.configure(api_key="AIzaSyARlUZKdVIfqER8S6aINQLhD1wdQhdTu-w")

# -----------------------------------------------------
# CONFIGURE OS DADOS DO SEU BANCO DE DADOS MYSQL AQUI
# -----------------------------------------------------
config_db = {
    'user': 'root',
    'password': 'seu_password_aqui',
    'host': '127.0.0.1',  # ou 'localhost'
    'database': 'CADASTRO'
}

# (Função do seu colega - INTACTA)
def gerar_feedback_ia(texto_base):
    """
    Gera um feedback motivacional e simpático para o aluno usando o modelo Gemini.
    """
    prompt_ia = (
        "Você é um tutor educacional simpático e motivacional. "
        "Transforme a frase abaixo em um parágrafo encorajador, com foco em como o aluno pode melhorar. "
        "Não use saudações nem despedidas. "
        f"Frase base: {texto_base}"
    )
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt_ia)
        return resposta.text.strip()
    except Exception as e:
        print(f"Erro na API Gemini: {e}")
        return f"[Erro ao gerar feedback com IA]"

# (Função do seu colega - INTACTA)
def analisar_desempenho(df, materias):
    """
    Processa o DataFrame, calcula a média, identifica a matéria a melhorar e gera feedback via IA.
    """
    print("Iniciando análise de desempenho...")

    # Garante que todas as matérias esperadas existam, preenchendo com 0 se faltar
    for materia in materias:
        if materia not in df.columns:
            df[materia] = 0.0

    df_materias = df[materias]
    
    df['Média'] = df_materias.mean(axis=1).round(1)
    df['Matéria a melhorar'] = df_materias.idxmin(axis=1)

    feedbacks = []
    for _, aluno in df.iterrows():
        # Pega a nota da matéria a melhorar
        materia_pior = aluno['Matéria a melhorar']
        nota_baixa = aluno[materia_pior]
        
        texto_base = (
            f"O aluno {aluno['Aluno']} tem média {aluno['Média']:.1f}. "
            f"Seu desempenho mais baixo foi em {materia_pior} com nota {nota_baixa:.1f}. "
            f"Recomenda-se focar mais nessa disciplina nas próximas semanas."
        )
        print(f"Gerando feedback para {aluno['Aluno']}...")
        feedback = gerar_feedback_ia(texto_base)
        feedbacks.append(feedback)

    df['Feedback IA'] = feedbacks
    print("Análise de desempenho concluída.")
    return df

# ------------------------------------------------------------------
# 2. NOVAS FUNÇÕES DE "PONTE" (SQL <-> PYTHON)
# ------------------------------------------------------------------

def buscar_dados_do_banco(conexao):
    """
    Busca os dados normalizados (formato "longo") do banco de dados.
    """
    print("Buscando dados no banco...")
    
    # Esta query é o coração da busca:
    # 1. Junta usuario, dados_aluno, turma_alunos, turmas e disciplinas
    # 2. Pega apenas o nome do aluno, nome da disciplina e a nota final
    # 3. Filtra apenas por usuários que são 'alunos' (id_nivel = 3)
    # 4. Filtra apenas as matérias que a IA espera
    
    # Lista de matérias que seu script de IA espera
    materias_ia = ['Matemática', 'Português', 'História', 'Ciências']
    
    # O formato string (%s, %s...) é para segurança (SQL Injection)
    query_sql = f"""
        SELECT 
            u.id_user,
            u.nome AS 'Aluno',
            d.nome_disciplina,
            ta.nota_final
        FROM 
            usuario u
        JOIN 
            dados_aluno da ON u.id_user = da.id_user
        JOIN 
            turma_alunos ta ON da.id_user = ta.id_aluno
        JOIN 
            turmas t ON ta.id_turma = t.id_turma
        JOIN 
            disciplinas d ON t.id_disciplina = d.id_disciplina
        WHERE 
            u.id_nivel = 3  -- 3 = 'aluno' (baseado no seu INSERT)
            AND d.nome_disciplina IN ({','.join(['%s'] * len(materias_ia))})
    """
    
    # O Pandas lê o SQL e já cria um DataFrame
    # O 'params' passa a lista de matérias de forma segura
    df_longo = pd.read_sql(query_sql, conexao, params=materias_ia)
    
    if df_longo.empty:
        print("Aviso: Nenhum dado de nota encontrado no banco para as matérias especificadas.")
        return pd.DataFrame(), materias_ia
        
    print(f"Encontrados {len(df_longo)} registros de notas.")
    
    # Agora, a mágica do "Pivot":
    # Transformar o formato "longo" em "largo"
    #
    # DE:
    # id_user | Aluno | nome_disciplina | nota_final
    # 1       | Maria | Matemática      | 5.5
    # 1       | Maria | Português       | 7.0
    #
    # PARA:
    # id_user | Aluno | Matemática | Português
    # 1       | Maria | 5.5        | 7.0
    
    print("Transformando dados (pivot)...")
    df_largo = df_longo.pivot_table(
        index=['id_user', 'Aluno'], 
        columns='nome_disciplina', 
        values='nota_final'
    ).reset_index()
    
    # Renomeia as colunas para o Pandas ficar feliz
    df_largo.columns.name = None 
    
    return df_largo, materias_ia

def salvar_feedbacks_no_banco(conexao, df_resultado):
    """
    Pega o DataFrame com os feedbacks e salva de volta no banco.
    """
    print(f"Salvando {len(df_resultado)} feedbacks no banco de dados...")
    cursor = conexao.cursor()
    
    query_update = """
        UPDATE dados_aluno 
        SET feedback_ia = %s 
        WHERE id_user = %s
    """
    
    # Prepara os dados para a atualização em massa
    dados_para_salvar = []
    for _, linha in df_resultado.iterrows():
        dados_para_salvar.append(
            (linha['Feedback IA'], linha['id_user'])
        )

    try:
        # Executa a atualização de vários registros de uma vez
        cursor.executemany(query_update, dados_para_salvar)
        conexao.commit()
        print(f"Sucesso! {cursor.rowcount} linhas atualizadas.")
        
    except Error as e:
        print(f"Erro ao salvar feedbacks no banco: {e}")
        conexao.rollback()
    finally:
        cursor.close()

# ------------------------------------------------------------------
# 3. FUNÇÃO PRINCIPAL (MAIN) - ORQUESTRADOR
# ------------------------------------------------------------------

def main():
    """
    Orquestra todo o processo de integração.
    """
    conexao = None
    try:
        # 1. Conectar ao Banco
        conexao = mysql.connector.connect(**config_db)
        if conexao.is_connected():
            print(f"Conectado ao banco de dados '{config_db['database']}' com sucesso!")
        
        # 2. Buscar e transformar os dados
        df_para_ia, materias = buscar_dados_do_banco(conexao)
        
        if df_para_ia.empty:
            print("Não há dados de alunos para processar. Encerrando.")
            return

        print("\n--- DataFrame pronto para a IA ---")
        print(df_para_ia)
        print("----------------------------------\n")

        # 3. Rodar a análise da IA (código do seu colega)
        df_resultado = analisar_desempenho(df_para_ia, materias)

        print("\n--- Resultado Final com Feedbacks ---")
        print(df_resultado[['Aluno', 'Média', 'Matéria a melhorar', 'Feedback IA']])
        print("-------------------------------------\n")

        # 4. Salvar os resultados de volta no Banco
        salvar_feedbacks_no_banco(conexao, df_resultado)

    except Error as e:
        print(f"Erro na conexão com o MySQL: {e}")
    
    finally:
        # 5. Fechar a conexão
        if conexao and conexao.is_connected():
            conexao.close()
            print("Conexão com o MySQL fechada.")

# Ponto de entrada do script
if __name__ == "__main__":
    main()