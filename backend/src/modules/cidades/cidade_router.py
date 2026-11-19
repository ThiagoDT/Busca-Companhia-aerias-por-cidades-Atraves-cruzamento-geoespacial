
from flask import Blueprint

from src.modules.cidades.cidade_controller import CidadeController


cidade_bp = Blueprint("cidades", __name__)


# Cadastrar cidade
cidade_bp.route(
    "/api/cidades",
    methods=["POST"]
)(CidadeController.cadastrar_cidade)


# Listar cidades
cidade_bp.route(
    "/api/cidades",
    methods=["GET"]
)(CidadeController.listar_cidades)


# Localizar cidade utilizando Nominatim
cidade_bp.route(
    "/api/cidades/localizar",
    methods=["GET"]
)(CidadeController.localizar_cidade)
