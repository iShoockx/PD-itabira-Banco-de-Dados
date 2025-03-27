
const btn_op1 = document.getElementById('op1');
const btn_op2 = document.getElementById('op2');
const input = document.getElementById('input');



btn_op1.addEventListener('click', async () => {
    const idrequerido = input.value.trim();
    buscarporid(idrequerido);
    input.value = "";
})
btn_op2.addEventListener('click', async () => {
    verificarponto();
})


function buscarporid(id) {

    fetch('partners.json')
        .then(response => response.json()) // Converte a resposta para JSON
        .then(dados => {
            let idencontrado = dados.pdvs.find(pdv => pdv.id === id);

            if (idencontrado) {
                console.log(idencontrado);
                let resultado1 = document.getElementById("resultado1");

                let htmlContent = ""; // Variável para armazenar os parágrafos gerados

                for (let chave in idencontrado) {
                    if (idencontrado.hasOwnProperty(chave)) {
                        if (typeof idencontrado[chave] === 'object') {
                            // Se for um objeto (como coverageArea ou address), formatar como JSON
                            htmlContent += `<p id="${chave}">${chave}: ${JSON.stringify(idencontrado[chave], null, 2)}</p>`;
                        } else {
                            // Se for um valor simples, exibir diretamente
                            htmlContent += `<p id="${chave}">${chave}: ${idencontrado[chave]}</p>`;
                        }
                    }
                }

                resultado1.innerHTML = htmlContent; // Atualiza o conteúdo de uma vez com todos os parágrafos

            } else {
                console.log("PDV não encontrado!");
                resultado1.innerHTML = "PDV não encontrado";
            }
        })
        .catch(error => console.error('Erro ao carregar o JSON:', error));


}


async function verificarponto() {
    const lat = parseFloat(document.getElementById('lat').value);
    const lng = parseFloat(document.getElementById('lng').value);

    if (isNaN(lat) || isNaN(lng)) {
        alert("Latitude ou Longitude inválida");
        return;
    }

    try {
        const response = await fetch("partners.json");
        const data = await response.json();

        console.log("Dados carregados:", data);

        // Criando o ponto corretamente
        const ponto = turf.point([lng,lat ]);

        let encontrado = false;
        let pdvEncontrado = null;

        data.pdvs.forEach(pdv => {
            console.log(`PDV: ${pdv.tradingName}`, pdv.coverageArea.coordinates);

            // ✅ Verifica se coverageArea.coordinates tem a estrutura correta
            if (!Array.isArray(pdv.coverageArea.coordinates)) {
                console.error(`Erro: coverageArea.coordinates não é um array!`, pdv.coverageArea.coordinates);
                return;
            }

            // ✅ Certifica-se de que todas as coordenadas são números válidos
            const multipolygon = turf.multiPolygon(
                pdv.coverageArea.coordinates.map(polygon => {
                    if (!Array.isArray(polygon)) {
                        console.error(`Erro: Polígono inválido`, polygon);
                        return [];
                    }

                    return polygon.map(ring => {
                        if (!Array.isArray(ring)) {
                            console.error(`Erro: Ring inválido`, ring);
                            return [];
                        }

                        return ring.map(coord => {
                            if (!Array.isArray(coord) || coord.length !== 2) {
                                console.error("Erro: Coordenada inválida!", coord);
                                return [0, 0]; // Para evitar quebrar o código
                            }
                            return [parseFloat(coord[0]), parseFloat(coord[1])];
                        });
                    });
                })
            );

            if (turf.booleanPointInPolygon(ponto, multipolygon)) {
                encontrado = true;
                pdvEncontrado = pdv;
            }
        });

        const resultado2 = document.getElementById("resultado2");
        if (encontrado) {
            resultado2.innerHTML = `<strong>PDV Encontrado:</strong> ${pdvEncontrado.tradingName}`;
        } else {
            resultado2.innerHTML = "<strong>PDV não encontrado na área!</strong>";
        }
    } catch (error) {
        console.error("Erro ao carregar o JSON:", error);
        alert("Erro ao carregar os dados!");
    }
}
