
import json
import math

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from src.modules.cidades.cidade_repository import CidadeRepository


class CidadeService:

    @staticmethod
    def cadastrar_cidade(dados):

        if not isinstance(dados, dict):
            raise ValueError("Os dados da cidade são inválidos.")

        nome = dados.get("nome")
        estado = dados.get("estado")
        pais = dados.get("pais", "Brasil")
        latitude = dados.get("latitude")
        longitude = dados.get("longitude")

        # Validar campos obrigatórios
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Informe o nome da cidade.")

        if not isinstance(estado, str) or not estado.strip():
            raise ValueError("Informe o estado da cidade.")

        if not isinstance(pais, str) or not pais.strip():
            raise ValueError("Informe o país.")

        if len(estado.strip()) != 2:
            raise ValueError("O estado deve possuir uma sigla de 2 letras.")

        # Validar coordenadas
        try:
            if isinstance(latitude, bool) or isinstance(longitude, bool):
                raise ValueError()

            latitude = float(latitude)
            longitude = float(longitude)

        except (TypeError, ValueError):
            raise ValueError("Latitude e longitude devem ser números.")

        if not math.isfinite(latitude) or not math.isfinite(longitude):
                raise ValueError("As coordenadas devem ser números finitos.")
                
        if not -90 <= latitude <= 90:
            raise ValueError("A latitude deve estar entre -90 e 90.")

        if not -180 <= longitude <= 180:
            raise ValueError("A longitude deve estar entre -180 e 180.")

        # Cadastrar cidade
        return CidadeRepository.cadastrar_cidade(
            nome.strip(),
            estado.strip().upper(),
            pais.strip(),
            latitude,
            longitude
        )
    @staticmethod
    def localizar_cidade(nome, estado, pais):
        # Validação dos dados
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Informe o nome da cidade.")

        if not isinstance(estado, str) or not estado.strip():
            raise ValueError("Informe o estado da cidade.")

        if not isinstance(pais, str) or not pais.strip():
            raise ValueError("Informe o país.")

        # Monta a consulta para o Nominatim
        parametros = urlencode({
            "city": nome.strip(),
            "state": estado.strip(),
            "country": pais.strip(),
            "format": "jsonv2",
            "limit": 5,
            "addressdetails": 1
        })

        url = f"https://nominatim.openstreetmap.org/search?{parametros}"

        requisicao = Request(
            url,
            headers={
                "User-Agent": "PRJ12-GeospatialApp/1.0 (contact: contato@exemplo.com)"
            }
        )

        try:
            with urlopen(requisicao, timeout=10) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))

            if not dados:
                raise ValueError(
                    "Não foi possível localizar essa cidade. "
                    "Confira o nome, estado e país."
                )

            # Retorna as informações do primeiro resultado
            resultado = dados[0]

            return {
                "nome": nome.strip(),
                "estado": estado.strip().upper(),
                "pais": pais.strip(),
                "latitude": float(resultado["lat"]),
                "longitude": float(resultado["lon"]),
                "localizacao": resultado["display_name"]
            }

        except HTTPError as error:
            print(f"Erro HTTP do Nominatim: {error.code}")
            raise RuntimeError("Erro ao consultar o serviço de localização.")

        except URLError as error:
            print(f"Erro de conexão com Nominatim: {error}")
            raise RuntimeError("Não foi possível conectar ao serviço de localização.")

        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            raise RuntimeError("O serviço de localização retornou dados inválidos.")

    @staticmethod
    def listar_cidades():
        return CidadeRepository.listar_cidades()
