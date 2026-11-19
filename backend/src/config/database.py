
import os
import psycopg2


def get_connection():

    # Verificar configurações obrigatórias
    variaveis = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD")
    }

    ausentes = [
        nome for nome, valor in variaveis.items()
        if not valor
    ]

    if ausentes:
        raise ValueError(
            f"Variáveis de ambiente não configuradas: {', '.join(ausentes)}"
        )

    try:
        connection = psycopg2.connect(
            host=variaveis["DB_HOST"],
            port=variaveis["DB_PORT"],
            database=variaveis["DB_NAME"],
            user=variaveis["DB_USER"],
            password=variaveis["DB_PASSWORD"]
        )

        return connection

    except psycopg2.Error as error:
        print(f"Erro ao conectar ao banco: {error}")
        raise
