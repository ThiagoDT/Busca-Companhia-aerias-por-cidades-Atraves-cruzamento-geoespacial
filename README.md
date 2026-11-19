# PRJ.12 – Sistema de Busca Geoespacial

## 1. Sobre o projeto

O PRJ.12 é um projeto desenvolvido para a disciplina de Matemática da Computação, com o objetivo de implementar uma aplicação de busca geoespacial utilizando um banco de dados PostgreSQL com a extensão PostGIS.

A aplicação permite que o usuário desenhe um polígono diretamente em um mapa interativo e realize uma consulta espacial para identificar quais cidades estão localizadas dentro da região selecionada.

Além da busca geoespacial, o sistema permite cadastrar novas cidades, localizar suas coordenadas geográficas automaticamente e visualizar as cidades cadastradas no mapa.

O projeto utiliza uma arquitetura organizada em camadas no backend, separando as responsabilidades de roteamento, controle, regras de negócio e acesso ao banco de dados.

## 2. Objetivos

- Implementar consultas geoespaciais utilizando PostgreSQL e PostGIS.
- Permitir a seleção de regiões por meio de polígonos em um mapa interativo.
- Identificar cidades localizadas dentro de uma região selecionada.
- Retornar informações relacionadas às cidades, como companhias aéreas e turnos.
- Permitir o cadastro e a listagem de cidades.
- Integrar frontend, backend e banco de dados utilizando Docker.

## 3. Tecnologias utilizadas

### Backend
- **Python 3.12:** linguagem utilizada no desenvolvimento do servidor.
- **Flask:** framework responsável pela criação da API REST.
- **Psycopg2:** biblioteca utilizada para comunicação com PostgreSQL.
- **Python-dotenv:** gerenciamento de variáveis de ambiente.

### Banco de dados
- **PostgreSQL 17:** sistema gerenciador de banco de dados relacional.
- **PostGIS 3.5:** extensão responsável pelo armazenamento e processamento de dados geográficos.

### Frontend
- **HTML5:** estrutura das páginas.
- **CSS3:** estilização da interface.
- **JavaScript:** interação com o mapa e comunicação com a API.
- **Leaflet:** biblioteca para exibição de mapas interativos.
- **Leaflet.draw:** ferramenta para desenhar e editar polígonos no mapa.
- **OpenStreetMap:** provedor dos mapas utilizados na aplicação.

### Infraestrutura
- **Docker:** criação e execução dos containers.
- **Docker Compose:** gerenciamento dos serviços da aplicação.
- **Nginx:** disponibilização do frontend e encaminhamento das requisições para o backend.

## 4. Arquitetura do projeto

O backend utiliza uma arquitetura em camadas, separando as responsabilidades de cada módulo.

```text
Projeto PRJ.12/
│
├── backend/
│   ├── src/
│   │   ├── app.py
│   │   ├── config/
│   │   │   └── database.py
│   │   │
│   │   └── modules/
│   │       ├── busca/
│   │       │   ├── busca_repository.py
│   │       │   ├── busca_service.py
│   │       │   ├── busca_controller.py
│   │       │   └── busca_router.py
│   │       │
│   │       └── cidades/
│   │           ├── cidade_repository.py
│   │           ├── cidade_service.py
│   │           ├── cidade_controller.py
│   │           └── cidade_router.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   │   └── map.js
│   ├── nginx.conf
│   └── Dockerfile
│
├── database/
│   └── scripts SQL de criação e população do banco
│
├── docker-compose.yml
├── .env.exemplo
├── .env
├── .gitignore
├── .dockerignore
└── README.md
```

### Responsabilidades das camadas

| Camada | Responsabilidade |
|---|---|
| Router | Define as rotas e os métodos HTTP disponíveis. |
| Controller | Recebe as requisições e retorna as respostas HTTP. |
| Service | Implementa as regras de negócio e valida os dados. |
| Repository | Executa as consultas SQL e acessa o banco de dados. |

Essa organização facilita a manutenção, a compreensão e a evolução do sistema.

## 5. Funcionamento da busca geoespacial

A busca geoespacial é a principal funcionalidade do projeto.

O usuário acessa o mapa e utiliza as ferramentas do Leaflet.draw para desenhar um polígono ou retângulo, delimitando uma região geográfica.

Após desenhar a região, o usuário clica no botão de busca. O frontend transforma a geometria selecionada em GeoJSON e envia os dados para o backend.

O backend valida a geometria e encaminha os dados para o Repository, que executa uma consulta espacial no PostgreSQL utilizando PostGIS.

### Fluxo da busca

1. O usuário desenha uma região no mapa.
2. O Leaflet transforma a região em GeoJSON.
3. O frontend envia uma requisição POST para a API.
4. O Controller recebe os dados.
5. O Service valida a geometria e suas coordenadas.
6. O Repository executa a consulta espacial no PostgreSQL.
7. O PostGIS identifica as cidades dentro do polígono.
8. O backend retorna os resultados em JSON.
9. O frontend apresenta os resultados em cards e marcadores no mapa.

### Consulta espacial

A principal função utilizada na consulta é:

```sql
ST_Within(
    c.localizacao,
    ST_SetSRID(
        ST_GeomFromGeoJSON(%s),
        4326
    )
)
```

Funções utilizadas:

- **ST_GeomFromGeoJSON():** converte o GeoJSON recebido em uma geometria reconhecida pelo PostGIS.
- **ST_SetSRID():** define o sistema de referência espacial utilizado, neste caso, EPSG:4326.
- **ST_Within():** verifica se a localização de uma cidade está dentro do polígono informado.
- **ST_X():** retorna a longitude de um ponto.
- **ST_Y():** retorna a latitude de um ponto.

A utilização dessas funções permite realizar o cruzamento espacial diretamente no banco de dados, sem precisar implementar os cálculos geográficos manualmente no Python.

**Observação:** o sistema trabalha com um polígono por vez. Ao desenhar uma nova região, o polígono anterior é substituído.

## 6. Funcionalidades

### 6.1. Busca geoespacial

Permite desenhar uma região no mapa e identificar as cidades localizadas dentro dela.

Os resultados apresentam:

- Nome da cidade.
- Estado.
- Companhias aéreas relacionadas.
- Turnos cadastrados.
- Marcadores das cidades encontradas no mapa.

Caso nenhuma cidade seja encontrada, o sistema informa que não existem resultados naquela região.

### 6.2. Cadastro de cidades

O sistema permite cadastrar novas cidades no banco de dados.

O processo funciona da seguinte maneira:

1. O usuário informa o nome da cidade, estado e país.
2. O sistema consulta o serviço de geolocalização Nominatim.
3. O serviço retorna as coordenadas geográficas.
4. O frontend apresenta a latitude e a longitude encontradas.
5. O usuário confirma o cadastro.
6. O backend valida os dados e salva a cidade no PostgreSQL.

O sistema também verifica se a cidade já está cadastrada, evitando registros duplicados.

### 6.3. Listagem de cidades

A aplicação consulta as cidades cadastradas no banco de dados e apresenta seus marcadores no mapa.

Cada marcador permite visualizar informações da cidade, como nome, estado e país.

### 6.4. Gerenciamento dos polígonos

O usuário pode:

- Desenhar um polígono.
- Desenhar um retângulo.
- Editar a região selecionada.
- Excluir a região desenhada.
- Substituir a região anterior por uma nova.

Quando a região é excluída, editada ou substituída, os resultados da busca anterior são removidos da interface.

## 7. Banco de dados

O banco de dados utiliza PostgreSQL com a extensão PostGIS para armazenar e consultar informações geográficas.

### Principais tabelas

| Tabela | Descrição |
|---|---|
| `cidades` | Armazena as cidades e suas coordenadas geográficas. |
| `companhias_aereas` | Armazena as companhias aéreas cadastradas. |
| `companhia_cidade` | Relaciona cidades e companhias aéreas. |
| `turnos` | Armazena os turnos relacionados às cidades. |

### Armazenamento geográfico

A tabela `cidades` possui uma coluna chamada `localizacao`, do tipo:

```sql
GEOMETRY(POINT, 4326)
```

Essa coluna armazena a localização geográfica de cada cidade.

O SRID 4326 representa o sistema de referência geográfica WGS84, utilizado para trabalhar com coordenadas de latitude e longitude.

## 8. API – Rotas disponíveis

### Busca geoespacial

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/busca/geoespacial` | Busca cidades dentro de um polígono. |

Exemplo de requisição:

```json
{
  "poligono": {
    "type": "Polygon",
    "coordinates": [
      [
        [-47.95, -15.80],
        [-47.85, -15.80],
        [-47.85, -15.70],
        [-47.95, -15.70],
        [-47.95, -15.80]
      ]
    ]
  }
}
```

### Cidades

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/cidades` | Lista as cidades cadastradas. |
| POST | `/api/cidades` | Cadastra uma nova cidade. |
| GET | `/api/cidades/localizar` | Localiza uma cidade e retorna suas coordenadas. |

Exemplo de cadastro:

```json
{
  "nome": "Santos",
  "estado": "SP",
  "pais": "Brasil",
  "latitude": -23.9609448,
  "longitude": -46.3166316
}
```

### Verificação da aplicação

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando. |
| GET | `/health` | Verifica a conexão com PostgreSQL e PostGIS. |

## 9. Como executar o projeto

### Pré-requisitos

Antes de iniciar, é necessário ter instalado:

- Docker.
- Docker Compose.

### Configuração das variáveis de ambiente

Na raiz do projeto, crie ou configure o arquivo `.env`:

```env
PORT_BACK=3500
PORT_FRONT=5600
PORT_DATABASE=5434

POSTGRES_USER=postgres
POSTGRES_DATABASE=prj12
POSTGRES_PASSWORD=sua_senha
```

Substitua `sua_senha` por uma senha segura.

### Construir e iniciar os containers

Na raiz do projeto, execute:

```bash
docker compose up -d --build
```

Esse comando constrói as imagens e inicia os serviços:

- PostgreSQL com PostGIS.
- Backend Flask.
- Frontend Nginx.

### Verificar os containers

```bash
docker compose ps
```

### Consultar os logs

```bash
docker compose logs -f
```

### Acessar a aplicação

Após a inicialização, acesse:

| Serviço | Endereço |
|---|---|
| Frontend | http://localhost:5600 |
| Backend | http://localhost:3500 |
| Verificação da API | http://localhost:3500/ |
| Saúde do banco | http://localhost:3500/health |
| PostgreSQL | localhost:5434 |

## 10. Tratamento de erros

O sistema possui tratamento de erros nas diferentes camadas da aplicação.

Alguns exemplos:

| Situação | Código HTTP |
|---|---|
| Requisição com dados inválidos | 400 |
| Cidade já cadastrada | 409 |
| Erro ao consultar serviço externo de localização | 502 |
| Erro interno no servidor | 500 |
| Operação realizada com sucesso | 200 ou 201 |

As respostas são retornadas em formato JSON, permitindo que o frontend apresente mensagens adequadas ao usuário.

## 11. Considerações finais

O PRJ.12 demonstra a aplicação de conceitos de Matemática da Computação e banco de dados geográficos por meio de uma aplicação web interativa.

A utilização do PostgreSQL com PostGIS permite realizar consultas espaciais diretamente no banco de dados, identificando cidades que pertencem a uma determinada região geográfica.

A integração entre Python, Flask, Leaflet e PostgreSQL possibilita desenvolver uma aplicação organizada, com separação de responsabilidades entre frontend, backend e banco de dados.

Além disso, o projeto demonstra como tecnologias de geolocalização podem ser utilizadas para solucionar problemas que envolvem localização, coordenadas e cruzamentos geográficos.

---

**Projeto:** PRJ.12 – Busca Geoespacial  
**Disciplina:** Matemática da Computação  
**Banco de dados:** PostgreSQL + PostGIS  
**Backend:** Python + Flask  
**Frontend:** HTML, CSS, JavaScript + Leaflet