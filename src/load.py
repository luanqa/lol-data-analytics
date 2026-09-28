import psycopg2
from psycopg2 import extras
import os
import api_test
PSW_BD = os.getenv("SENHA_BANCO")

# 1. Configurações de conexão com o banco de dados
DB_HOST = "localhost"
DB_NAME = "lol_analytics"
DB_USER = "postgres"
DB_PASSWORD = PSW_BD
DB_PORT = "5432"

def carregar_dados():
    conexao = None
    cursor = None
    try:
        # 2. Estabelecendo a conexão
        conexao = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        # Criando o cursor para executar os comandos SQL
        cursor = conexao.cursor()

        # 3. Dados fictícios que serão inseridos (lista de tuplas)
        dados_para_inserir = [
            ('Ana Souza', 'ana@email.com', 28),
            ('Carlos Lima', 'carlos@email.com', 34),
            ('Mariana Costa', 'mariana@email.com', 22)
        ]

        dados = api_test.partida()


        # 4. Comando SQL com placeholders (%s) para evitar SQL Injection
        comando_sql = "INSERT INTO usuarios (nome, email, idade) VALUES (%s, %s, %s);"

        # 5. Executando a inserção em lote (Múltiplos dados de uma vez)
        cursor.executemany(comando_sql, dados_para_inserir)

        # 6. Salvando as alterações no banco de dados
        conexao.commit()
        print(f"{len(dados_para_inserir)} registros inseridos com sucesso!")

    except Exception as erro:
        # Desfaz as alterações caso ocorra algum erro durante o processo
        if conexao:
            conexao.rollback()
        print(f"Erro ao inserir dados: {erro}")

    finally:
        # 7. Garantindo o fechamento das conexões
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def teste():
    dados = api_test.partida()
    dados_jogador = dados[2]
    dados_insert  = []
    chaves = list(dados_jogador.keys())
    valores = list(dados_jogador.values())
    print (valores)

    comando_sql = "INSERT INTO usuarios (puuid, nome, tag) VALUES (%s, %s, %s);"
    
    # 5. Executando a inserção em lote (Múltiplos dados de uma vez)
    cursor.executemany(comando_sql, valores)

