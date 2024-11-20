/*Animação Para Registro de Conta*/
document.addEventListener("DOMContentLoaded", function () {
  const register = document.querySelector(".register");

  function checkVisibility() {
    var windowHeight = window.innerHeight;
    var scrollY = window.scrollY || window.pageYOffset;
    var registerOffsetTop = register.offsetTop;

    if (
      scrollY + windowHeight >= registerOffsetTop &&
      scrollY <= registerOffsetTop + register.offsetHeight
    ) {
      register.classList.add("visible");
    }
  }

  window.addEventListener("scroll", checkVisibility);
  checkVisibility(); // Verifica a visibilidade ao carregar a página
});
