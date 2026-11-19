let locatedCity = null;
const map = L.map("map").setView([-15.7801, -47.9292], 4);

// Camada do OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Grupo de polígonos desenhados
const drawnItems = new L.FeatureGroup();

map.addLayer(drawnItems);

// Configuração da ferramenta de desenho
const drawControl = new L.Control.Draw({
    draw: {
        polygon: true,
        rectangle: true,
        polyline: false,
        circle: false,
        circlemarker: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems
    }
});

map.addControl(drawControl);

// Marcadores de cidades cadastradas no banco
let registeredCityMarkers = [];

// Marcadores das cidades encontradas na busca geoespacial
let cityMarkers = [];

// Limpa os resultados da busca geoespacial
function limparResultados() {
    const results = document.getElementById("results");

    // Remove os cards exibidos
    results.innerHTML = "";

    // Remove somente os marcadores criados pela busca
    cityMarkers.forEach(marker => {
        map.removeLayer(marker);
    });

    cityMarkers = [];
}

// Busca todas as cidades cadastradas no banco
async function carregarCidades() {
    try {
        const response = await fetch("/api/cidades");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao carregar cidades.");
        }

        // Remove os marcadores cadastrados anteriormente
        registeredCityMarkers.forEach(marker => {
            map.removeLayer(marker);
        });

        registeredCityMarkers = [];

        // Cria um marcador para cada cidade
        data.cidades.forEach(cidade => {
            const marker = L.marker([
                cidade.latitude,
                cidade.longitude
            ]).addTo(map);

            marker.bindPopup(`
                <strong>${cidade.nome}</strong><br>
                Estado: ${cidade.estado}<br>
                País: ${cidade.pais}
            `);

            registeredCityMarkers.push(marker);
        });

    } catch (error) {
        console.error("Erro ao carregar cidades:", error);
    }
}

// Evento disparado quando um polígono é criado
map.on(L.Draw.Event.CREATED, function (event) {
    // Limpa os resultados da busca anterior
    limparResultados();

    // Remove os polígonos anteriores
    drawnItems.clearLayers();

    // Adiciona o novo polígono
    drawnItems.addLayer(event.layer);
});

// Quando um polígono é editado
map.on(L.Draw.Event.EDITED, function () {
    limparResultados();
});

// Limpa os resultados quando um polígono é excluído
map.on(L.Draw.Event.DELETED, function () {
    limparResultados();
});

// Botão de busca
document.getElementById("search-button").addEventListener("click", buscarCidades);

async function buscarCidades() {
    const layers = drawnItems.getLayers();

    if (layers.length === 0) {
        alert("Desenhe uma região no mapa primeiro.");
        return;
    }

    const polygon = layers[0].toGeoJSON().geometry;

    const button = document.getElementById("search-button");
    const results = document.getElementById("results");

    button.disabled = true;
    results.innerHTML = "<p>Buscando cidades...</p>";

    try {
        const response = await fetch(
            "/api/busca/geoespacial",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    poligono: polygon
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro na busca.");
        }

        exibirResultados(data);

    } catch (error) {
        console.error(error);

        results.innerHTML = `<p>${error.message}</p>`;

    } finally {
        button.disabled = false;
    }
}

function exibirResultados(data) {
    const results = document.getElementById("results");

    // Remove marcadores anteriores
    cityMarkers.forEach(marker => map.removeLayer(marker));
    cityMarkers = [];

    if (data.total === 0) {
        results.innerHTML = "<p>Nenhuma cidade encontrada nessa região.</p>";
        return;
    }

    results.innerHTML = `<p>Total de cidades encontradas: ${data.total}</p>`;

    data.cidades.forEach(cidade => {
        const card = document.createElement("div");

        card.className = "city-card";

        const title = document.createElement("h3");
        title.textContent = `${cidade.cidade} - ${cidade.estado}`;

        const airlines = document.createElement("p");
        airlines.textContent = `Companhias aéreas: ${cidade.companhias.join(", ") || "Nenhuma"}`;

        const shifts = document.createElement("p");
        shifts.textContent = `Turnos: ${cidade.turnos.join(", ") || "Nenhum"}`;

        card.append(title, airlines, shifts);
        results.appendChild(card);

        // Adiciona marcador no mapa
        const marker = L.marker([
            cidade.latitude,
            cidade.longitude
        ]).addTo(map);

        marker.bindPopup(`
            <strong>${cidade.cidade}</strong><br>
            Companhias: ${cidade.companhias.join(", ")}<br>
            Turnos: ${cidade.turnos.join(", ")}
        `);

        cityMarkers.push(marker);
    });

    // Ajusta o mapa para mostrar as cidades encontradas
    if (cityMarkers.length > 0) {
        const group = L.featureGroup(cityMarkers);
        map.fitBounds(group.getBounds().pad(0.2));
    }
}
async function localizarCidade() {
    const nome = document.getElementById("city-name").value.trim();
    const estado = document.getElementById("city-state").value.trim();
    const pais = document.getElementById("city-country").value.trim();

    const button = document.getElementById("locate-city-button");
    const status = document.getElementById("location-status");
    const preview = document.getElementById("coordinates-preview");
    const registerButton = document.getElementById("register-city-button");

    // Limpa uma localização anterior
    locatedCity = null;
    registerButton.disabled = true;
    preview.hidden = true;

    if (!nome || !estado || !pais) {
        status.textContent = "Preencha o nome, estado e país.";
        return;
    }

    button.disabled = true;
    status.textContent = "Localizando cidade...";

    try {
        const parametros = new URLSearchParams({
            nome,
            estado,
            pais
        });

        const response = await fetch(
            `/api/cidades/localizar?${parametros.toString()}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Não foi possível localizar a cidade.");
        }

        locatedCity = data;

        document.getElementById("latitude-preview").textContent =
            `Latitude: ${data.latitude}`;

        document.getElementById("longitude-preview").textContent =
            `Longitude: ${data.longitude}`;

        preview.hidden = false;
        registerButton.disabled = false;

        status.textContent = "Cidade localizada com sucesso!";

        // Centraliza o mapa na cidade encontrada
        map.setView(
            [data.latitude, data.longitude],
            10
        );

    } catch (error) {
        console.error("Erro ao localizar cidade:", error);
        status.textContent = error.message;

    } finally {
        button.disabled = false;
    }
}

document
    .getElementById("locate-city-button")
    .addEventListener("click", localizarCidade);
//cadastra a cidade
async function cadastrarCidade(event) {
    event.preventDefault();

    const registerButton = document.getElementById("register-city-button");
    const status = document.getElementById("location-status");

    if (!locatedCity) {
        status.textContent = "Primeiro localize a cidade.";
        return;
    }

    registerButton.disabled = true;
    status.textContent = "Cadastrando cidade...";

    try {
        const response = await fetch("/api/cidades", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: locatedCity.nome,
                estado: locatedCity.estado,
                pais: locatedCity.pais,
                latitude: locatedCity.latitude,
                longitude: locatedCity.longitude
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao cadastrar cidade.");
        }

        status.textContent = "Cidade cadastrada com sucesso!";

        // Atualiza os marcadores com os dados do banco
        await carregarCidades();

        // Limpa o formulário
        document.getElementById("city-form").reset();

        // Limpa os dados da localização anterior
        locatedCity = null;

        document.getElementById("coordinates-preview").hidden = true;

        registerButton.disabled = true;

    } catch (error) {
        console.error("Erro ao cadastrar cidade:", error);
        status.textContent = error.message;

    } finally {
        registerButton.disabled = true;
    }
}

document
    .getElementById("city-form")
    .addEventListener("submit", cadastrarCidade);

// Carrega as cidades assim que o mapa é inicializado
carregarCidades();