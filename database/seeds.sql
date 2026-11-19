
-- =====================================
-- 1. COMPANHIAS AÉREAS
-- =====================================

INSERT INTO companhias_aereas (nome)
VALUES
    ('LATAM'),
    ('GOL'),
    ('AZUL');

-- =====================================
-- 2. CIDADES
-- Coordenadas: longitude, latitude
-- =====================================

INSERT INTO cidades (nome, estado, pais, localizacao)
VALUES
    ('Sao Paulo', 'SP', 'Brasil',
     ST_SetSRID(ST_MakePoint(-46.6333, -23.5505), 4326)),

    ('Campinas', 'SP', 'Brasil',
     ST_SetSRID(ST_MakePoint(-47.0608, -22.9056), 4326)),

    ('Manaus', 'AM', 'Brasil',
     ST_SetSRID(ST_MakePoint(-60.0217, -3.1190), 4326)),

    ('Belem', 'PA', 'Brasil',
     ST_SetSRID(ST_MakePoint(-48.4902, -1.4558), 4326)),

    ('Rio de Janeiro', 'RJ', 'Brasil',
     ST_SetSRID(ST_MakePoint(-43.1729, -22.9068), 4326)),

    ('Curitiba', 'PR', 'Brasil',
     ST_SetSRID(ST_MakePoint(-49.2733, -25.4284), 4326));

-- =====================================
-- 3. COMPANHIAS E CIDADES
-- =====================================

INSERT INTO companhia_cidade (id_companhia, id_cidade)
SELECT ca.id_companhia, c.id_cidade
FROM (VALUES
    ('LATAM', 'Sao Paulo'),
    ('LATAM', 'Belem'),
    ('LATAM', 'Curitiba'),
    ('GOL', 'Belem'),
    ('GOL', 'Manaus'),
    ('GOL', 'Rio de Janeiro'),
    ('AZUL', 'Campinas'),
    ('AZUL', 'Sao Paulo'),
    ('AZUL', 'Curitiba')
) AS dados(companhia, cidade)
JOIN companhias_aereas ca ON ca.nome = dados.companhia
JOIN cidades c ON c.nome = dados.cidade;

-- =====================================
-- 4. TURNOS DAS CIDADES
-- =====================================

INSERT INTO turnos (id_cidade, periodo)
SELECT c.id_cidade, dados.periodo
FROM (VALUES
    ('Sao Paulo', 'manha'),
    ('Sao Paulo', 'tarde'),
    ('Campinas', 'noite'),
    ('Manaus', 'manha'),
    ('Manaus', 'noite'),
    ('Belem', 'manha'),
    ('Belem', 'tarde'),
    ('Rio de Janeiro', 'tarde'),
    ('Rio de Janeiro', 'noite'),
    ('Curitiba', 'noite')
) AS dados(cidade, periodo)
JOIN cidades c ON c.nome = dados.cidade;
