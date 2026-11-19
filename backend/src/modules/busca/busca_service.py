
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

        cidades = BuscaRepository.buscar_cidades_por_poligono(
            poligono
        )

        return {
            "total": len(cidades),
            "cidades": cidades
        }
