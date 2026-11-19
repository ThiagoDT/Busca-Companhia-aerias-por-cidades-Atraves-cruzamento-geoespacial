
from psycopg2.extras import RealDictCursor

from src.config.database import get_connection


class CidadeRepository:

    @staticmethod
    def cadastrar_cidade(nome, estado, pais, latitude, longitude):

        sql = """
            INSERT INTO cidades (
                nome,
                estado,
                pais,
                localizacao
            )
            VALUES (
                %s,
                %s,
                %s,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )
            )
            RETURNING
                id_cidade,
                nome,
                estado,
                pais,
                ST_Y(localizacao) AS latitude,
                ST_X(localizacao) AS longitude;
        """

        connection = None

        try:
            connection = get_connection()

            with connection.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(
                    sql,
                    (
                        nome,
                        estado,
                        pais,
                        longitude,
                        latitude
                    )
                )

                cidade = cursor.fetchone()

            connection.commit()

            return cidade

        except Exception as error:
            if connection:
                connection.rollback()

            if getattr(error, "pgcode", None) == "23505":
                raise CidadeDuplicadaError("Essa cidade já está cadastrada.")

            raise

        finally:
            if connection:
                connection.close()


    @staticmethod
    def listar_cidades():
        sql = """
            SELECT
                id_cidade,
                nome,
                estado,
                pais,
                ST_Y(localizacao) AS latitude,
                ST_X(localizacao) AS longitude
            FROM cidades
            ORDER BY nome;
        """

        connection = None

        try:
            connection = get_connection()

            with connection.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(sql)
                cidades = cursor.fetchall()

                return cidades

        finally:
            if connection:
                connection.close()

#Classe de excessão
class CidadeDuplicadaError(Exception):
    pass