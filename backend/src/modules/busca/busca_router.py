
from flask import Blueprint

from src.modules.busca.busca_controller import BuscaController


busca_bp = Blueprint("busca", __name__)

busca_bp.route(
    "/api/busca/geoespacial",
    methods=["POST"]
)(BuscaController.buscar_geoespacial)
