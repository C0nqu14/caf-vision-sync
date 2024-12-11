/*Menu Home*/
document.addEventListener("DOMContentLoaded", function () {
  var addBtn = document.querySelector(".toggle-menu");
  var removeBtn = document.querySelector(".close-menu");
  var sidebarDropdown = document.querySelector(".sidebar-dropdown");

  addBtn.addEventListener("click", function () {
    sidebarDropdown.classList.toggle("active");
    addBtn.style.display = "none";
    removeBtn.style.display = "block";
  });

  removeBtn.addEventListener("click", function () {
    sidebarDropdown.classList.remove("active");
    removeBtn.style.display = "none";
    addBtn.style.display = "block";
  });
});

/* Menu do Feedback */
document.addEventListener("DOMContentLoaded", () => {
  const openMenuIcon = document.getElementById("open_menu");
  const closeMenuIcon = document.getElementById("close_menu");
  const containerLeft = document.getElementById("container-left");
  const containerRight = document.getElementById("container-right");

  containerLeft.style.transition = "width 0.3s ease, transform 0.3s ease";
  containerRight.style.transition = "width 0.3s ease";

  // Função para ajustar o layout com base no tamanho da tela
  const adjustLayout = () => {
    if (window.innerWidth > 1024) {
      containerLeft.style.display = "flex";
      containerLeft.style.width = "25%";
      containerLeft.style.transform = "translateX(0)";
      containerRight.style.width = "75%";
      openMenuIcon.style.display = "none";
    } else {
      // Em telas menores, o menu começa oculto
      containerLeft.style.display = "none";
      containerRight.style.width = "100%";
      openMenuIcon.style.display = "flex";
    }
  };

  // Evento de clique para abrir o menu
  openMenuIcon.addEventListener("click", () => {
    containerLeft.style.display = "flex"; // Mostrar o menu
    setTimeout(() => {
      // Ajustar largura do menu com base no tamanho da tela
      if (window.innerWidth > 1024) {
        containerLeft.style.width = "25%";
        containerRight.style.width = "75%";
      } else {
        containerLeft.style.width = "60%";
        containerRight.style.width = "100%"; // Sempre 100% em telas menores
      }
      containerLeft.style.transform = "translateX(0)"; // Garantir que aparece suavemente
    }, 10); // Adiciona um pequeno delay para ativar a transição

    openMenuIcon.style.display = "none";
  });

  // Evento de clique para fechar o menu
  closeMenuIcon.addEventListener("click", () => {
    containerLeft.style.width = "0";
    containerLeft.style.transform = "translateX(-100%)";

    setTimeout(() => {
      containerLeft.style.display = "none"; // Remover do fluxo após a transição
    }, 300); // Tempo sincronizado com a transição

    containerRight.style.width = "100%";
    openMenuIcon.style.display = "flex";
  });

  // Ajustar layout no carregamento inicial
  adjustLayout();

  // Ajustar layout em redimensionamento da janela
  window.addEventListener("resize", adjustLayout);
});
