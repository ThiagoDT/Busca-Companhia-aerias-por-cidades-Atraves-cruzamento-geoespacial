
from flask import Flask, jsonify

from src.config.database import get_connection
from src.modules.busca.busca_router import busca_bp
from src.modules.cidades.cidade_router import cidade_bp


app = Flask(__name__)

# Registro das rotas
app.register_blueprint(busca_bp)
app.register_blueprint(cidade_bp)


# Rota para verificar o funcionamento do container e do banco
@app.route("/health", methods=["GET"])
def health():
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_Full_Version();")
            postgis_version = cursor.fetchone()[0]

        return jsonify({
            "status": "online",
            "database": "connected",
            "postgis": postgis_version
        }), 200

    except Exception as error:
        print(f"Erro na verificação de saúde: {error}")

        return jsonify({
            "status": "error",
            "database": "disconnected",
            "erro": "Não foi possível conectar ao banco de dados."
        }), 503

    finally:
        if connection:
            connection.close()


# Rota inicial
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API PRJ12 funcionando!",
        "status": "online"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3500,
        debug=True
    )
