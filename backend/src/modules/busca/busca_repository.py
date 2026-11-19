
import json

from psycopg2.extras import RealDictCursor

from src.config.database import get_connection


class BuscaRepository:

    @staticmethod
    def buscar_cidades_por_poligono(poligono):
        sql = """
            SELECT
                c.id_cidade,
                c.nome AS cidade,
                c.estado,
                ST_Y(c.localizacao) AS latitude,
                ST_X(c.localizacao) AS longitude,

                COALESCE(
                    jsonb_agg(DISTINCT ca.nome)
                    FILTER (WHERE ca.id_companhia IS NOT NULL),
                    '[]'::jsonb
                ) AS companhias,

                COALESCE(
                    jsonb_agg(DISTINCT t.periodo)
                    FILTER (WHERE t.id_turno IS NOT NULL),
                    '[]'::jsonb
                ) AS turnos

            FROM cidades c

            LEFT JOIN companhia_cidade cc
                ON cc.id_cidade = c.id_cidade

            LEFT JOIN companhias_aereas ca
                ON ca.id_companhia = cc.id_companhia

            LEFT JOIN turnos t
                ON t.id_cidade = c.id_cidade

            WHERE ST_Within(
                c.localizacao,
                ST_SetSRID(
                    ST_GeomFromGeoJSON(%s),
                    4326
                )
            )

            GROUP BY
                c.id_cidade,
                c.nome,
                c.estado,
                c.localizacao

            ORDER BY c.nome;
        """

        connection = None

        try:
            connection = get_connection()

            with connection.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(sql, (json.dumps(poligono),))

                return cursor.fetchall()

        finally:
            if connection:
                connection.close()
