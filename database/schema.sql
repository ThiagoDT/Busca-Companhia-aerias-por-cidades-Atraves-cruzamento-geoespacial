CREATE EXTENSION IF NOT EXISTS postgis;

SELECT PostGIS_Full_Version();
-- Tabela de companhias aéreas
CREATE TABLE companhias_aereas (
    id_companhia INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de cidades
CREATE TABLE cidades (
    id_cidade INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    pais VARCHAR(60) NOT NULL DEFAULT 'Brasil',
    localizacao GEOMETRY(POINT, 4326) NOT NULL,

    CONSTRAINT uq_cidade_estado_pais
        UNIQUE (nome, estado, pais)
);

-- Relacionamento entre companhias e cidades
CREATE TABLE companhia_cidade (
    id_companhia INTEGER NOT NULL,
    id_cidade INTEGER NOT NULL,

    PRIMARY KEY (id_companhia, id_cidade),

    FOREIGN KEY (id_companhia)
        REFERENCES companhias_aereas(id_companhia),

    FOREIGN KEY (id_cidade)
        REFERENCES cidades(id_cidade)
);

-- Turnos de operação das cidades
CREATE TABLE turnos (
    id_turno INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cidade INTEGER NOT NULL,
    periodo VARCHAR(20) NOT NULL,

    FOREIGN KEY (id_cidade)
        REFERENCES cidades(id_cidade),

    CONSTRAINT chk_periodo
        CHECK (periodo IN ('manha', 'tarde', 'noite')),

    CONSTRAINT uq_turno_cidade
        UNIQUE (id_cidade, periodo)
);
