
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

// Armazenará os marcadores das cidades
let cityMarkers = [];

// Evento disparado quando um polígono é criado
map.on(L.Draw.Event.CREATED, function (event) {
    drawnItems.clearLayers();
    drawnItems.addLayer(event.layer);
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
