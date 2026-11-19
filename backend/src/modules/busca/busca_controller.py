
from flask import jsonify, request

from src.modules.busca.busca_service import BuscaService


class BuscaController:

    @staticmethod
    def buscar_geoespacial():

        dados = request.get_json(silent=True)

        if not dados or "poligono" not in dados:
            return jsonify({
                "erro": "Informe um polígono."
            }), 400

        try:
            resultado = BuscaService.buscar_por_poligono(
                dados["poligono"]
            )

            return jsonify(resultado), 200

        except ValueError as error:
            return jsonify({
                "erro": str(error)
            }), 400

        except Exception as error:
            print(f"Erro na busca: {error}")

            return jsonify({
                "erro": "Erro interno ao realizar a busca."
            }), 500
