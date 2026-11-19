
import os
import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        return connection

    except psycopg2.Error as error:
        print(f"Erro ao conectar ao banco: {error}")
        raise
