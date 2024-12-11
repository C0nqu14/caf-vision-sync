document.addEventListener("DOMContentLoaded", () => {
  const todoHistorico = document.getElementById("all-history");

  const dadosDoBanco = [
    { data: "2024-12-10", historico: ["Histórico 1", "Histórico 2"] },
    { data: "2024-12-09", historico: ["Histórico 3"] },
    { data: "2024-12-10", historico: ["Histórico 4"] },
  ];

  // Função para formatar a data como 'Hoje', 'Ontem' ou 'YYYY-MM-DD'
  const formatarData = (data) => {
    const hoje = new Date();
    const dataHistorico = new Date(data);

    const diferencaTempo = hoje - dataHistorico;
    const diferencaDias = Math.ceil(diferencaTempo / (1000 * 60 * 60 * 24));

    if (diferencaDias === 0) return "Hoje";
    if (diferencaDias === 1) return "Ontem";
    return data;
  };

  // Função para deletar histórico
  const deletarHistorico = (icone) => {
    const historicoDiv = icone.closest(".history");
    historicoDiv.remove();
  };

  // Função para criar um container de histórico
  const criarContainerHistorico = (data, historicos) => {
    // Criar o container principal
    const container = document.createElement("div");
    container.classList.add("history-container");

    // Adicionar a data
    const divData = document.createElement("div");
    divData.classList.add("date");
    const paragrafoData = document.createElement("p");
    paragrafoData.id = "time-date";
    paragrafoData.textContent = formatarData(data);
    divData.appendChild(paragrafoData);
    container.appendChild(divData);

    // Adicionar os históricos
    historicos.forEach((historico) => {
      const divHistorico = document.createElement("div");
      divHistorico.classList.add("history");

      const linkHistorico = document.createElement("a");
      linkHistorico.href = "#";
      linkHistorico.textContent = historico;

      const iconeSpan = document.createElement("span");
      iconeSpan.classList.add("icon");
      iconeSpan.innerHTML = '<ion-icon name="ios-backspace"></ion-icon>';

      // Adicionar evento de clique no ícone para deletar
      const icone = iconeSpan.querySelector("ion-icon");
      icone.addEventListener("click", () => deletarHistorico(icone));

      divHistorico.appendChild(linkHistorico);
      divHistorico.appendChild(iconeSpan);
      container.appendChild(divHistorico);
    });

    return container;
  };

  // Agrupar os históricos pelo mesmo dia
  const dadosAgrupados = dadosDoBanco.reduce((acumulador, atual) => {
    if (!acumulador[atual.data]) acumulador[atual.data] = [];
    acumulador[atual.data].push(...atual.historico);
    return acumulador;
  }, {});

  // Criar os containers de histórico
  Object.entries(dadosAgrupados).forEach(([data, historicos]) => {
    const container = criarContainerHistorico(data, historicos);
    todoHistorico.appendChild(container);
  });
});
