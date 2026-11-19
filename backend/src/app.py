
from flask import Flask, jsonify
from src.config.database import get_connection
from src.modules.busca.busca_router import busca_bp

app = Flask(__name__)

app.register_blueprint(busca_bp)


#rota para verificar se o conteiner esta funcionando
@app.route("/health", methods=["GET"])
def health():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT PostGIS_Full_Version();")
        postgis_version = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            "status": "online",
            "database": "connected",
            "postgis": postgis_version
        }), 200

    finally:
        connection.close()

#Rota Inicial
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API PRJ12 funcionando!",
        "status": "online"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500, debug=True)
