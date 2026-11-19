
import math

from src.modules.busca.busca_repository import BuscaRepository


class BuscaService:

    @staticmethod
    def buscar_por_poligono(poligono):

        if not isinstance(poligono, dict):
            raise ValueError("O polígono deve ser um objeto GeoJSON.")

        if poligono.get("type") != "Polygon":
            raise ValueError("A geometria deve ser do tipo Polygon.")

        coordenadas = poligono.get("coordinates")

        if not isinstance(coordenadas, list) or not coordenadas:
            raise ValueError("O polígono precisa possuir coordenadas.")

        # Validar cada anel do polígono
        for anel in coordenadas:

            if not isinstance(anel, list) or len(anel) < 4:
                raise ValueError(
                    "Cada anel do polígono precisa possuir pelo menos quatro posições."
                )

            # Validar cada posição
            for posicao in anel:

                if not isinstance(posicao, list) or len(posicao) < 2:
                    raise ValueError(
                        "Cada posição deve possuir longitude e latitude."
                    )

                longitude, latitude = posicao[:2]

                if (
                    isinstance(longitude, bool)
                    or isinstance(latitude, bool)
                    or not isinstance(longitude, (int, float))
                    or not isinstance(latitude, (int, float))
                ):
                    raise ValueError(
                        "Longitude e latitude devem ser números."
                    )

                if not math.isfinite(longitude) or not math.isfinite(latitude):
                    raise ValueError(
                        "As coordenadas devem ser números finitos."
                    )

                if not -180 <= longitude <= 180:
                    raise ValueError("Longitude fora dos limites permitidos.")

                if not -90 <= latitude <= 90:
                    raise ValueError("Latitude fora dos limites permitidos.")

            # O anel precisa começar e terminar na mesma posição
            if anel[0] != anel[-1]:
                raise ValueError(
                    "O anel do polígono precisa ser fechado."
                )

        cidades = BuscaRepository.buscar_cidades_por_poligono(
            poligono
        )

        return {
            "total": len(cidades),
            "cidades": cidades
        }
