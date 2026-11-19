
from flask import jsonify, request

from src.modules.cidades.cidade_service import CidadeService
from src.modules.cidades.cidade_repository import CidadeDuplicadaError

class CidadeController:

    @staticmethod
    #caminho que cadastra as cidades
    def cadastrar_cidade():

        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({
                "erro": "Informe os dados da cidade em formato JSON."
            }), 400

        try:
            cidade = CidadeService.cadastrar_cidade(dados)

            return jsonify({
                "mensagem": "Cidade cadastrada com sucesso.",
                "cidade": cidade
            }), 201

        except CidadeDuplicadaError as error:
            return jsonify({"erro": str(error)}), 409

        except ValueError as error:
            return jsonify({"erro": str(error)}), 400

        except Exception as error:
            print(f"Erro ao cadastrar cidade: {error}")
            return jsonify({
                "erro": "Não foi possível cadastrar a cidade."
            }), 500

    #Caminho que mostra todas a cidade cadastradas
    @staticmethod
    def listar_cidades():
        try:
            cidades = CidadeService.listar_cidades()

            return jsonify({
                "total": len(cidades),
                "cidades": cidades
            }), 200

        except Exception as error:
            print(f"Erro ao listar cidades: {error}")

            return jsonify({
                "erro": "Não foi possível listar as cidades."
            }), 500
    #caminho que localiza cidade
    @staticmethod
    def localizar_cidade():
        nome = request.args.get("nome")
        estado = request.args.get("estado")
        pais = request.args.get("pais", "Brasil")

        try:
            resultado = CidadeService.localizar_cidade(
                nome,
                estado,
                pais
            )

            return jsonify(resultado), 200

        except ValueError as error:
            return jsonify({
                "erro": str(error)
            }), 400

        except RuntimeError as error:
            print(f"Erro na geocodificação: {error}")

            return jsonify({
                "erro": str(error)
            }), 502

        except Exception as error:
            print(f"Erro inesperado ao localizar cidade: {error}")

            return jsonify({
                "erro": "Não foi possível localizar a cidade."
            }), 500

