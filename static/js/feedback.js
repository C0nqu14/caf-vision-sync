document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.getElementById("textarea");
  const btnGravar = document.getElementById("mic-on");
  const btnParar = document.getElementById("mic-off");
  const sendButton = document.getElementById("send-sms");
  const messageContainer = document.getElementById("message-container");
  const welcomeMessage = document.getElementById("welcome-message");
  const message = "Bem-vindo ao CAF SYNC";
  const typingEffect = document.getElementById("typing-effect");
  let index = 0;

  function typeLetter() {
    if (index < message.length) {
      typingEffect.textContent += message.charAt(index);
      index++;
      setTimeout(typeLetter, 100);
    }
  }
  typeLetter();

  btnParar.style.display = "none";

  class SpeechAPI {
    constructor() {
      const SpeechText =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      this.speechAPI = new SpeechText();
      this.output = textarea;
      this.speechAPI.continuous = true;
      this.speechAPI.lang = "pt-PT";

      this.speechAPI.onresult = (e) => {
        let transcript = e.results[e.resultIndex][0].transcript;
        this.output.value += transcript;
      };
    }

    start() {
      this.speechAPI.start();
    }

    stop() {
      this.speechAPI.stop();
    }
  }

  let speech = new SpeechAPI();

  btnGravar.addEventListener("click", () => {
    btnGravar.style.display = "none";
    btnParar.style.display = "block";
    speech.start();
  });

  btnParar.addEventListener("click", () => {
    btnParar.style.display = "none";
    btnGravar.style.display = "block";
    speech.stop();
  });

  function createMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message";

    const senderDiv = document.createElement("div");
    senderDiv.id = sender;

    const cardDiv = document.createElement("div");
    cardDiv.className = sender === "message-person" ? "card" : "card-boot";

    if (sender === "message-boot") {
      const botImg = document.createElement("img");
      botImg.src = "../img/icons/favicon.png";
      botImg.alt = "icon-boot";
      cardDiv.appendChild(botImg);
    }

    const messageText = document.createElement("p");
    messageText.textContent = content;

    cardDiv.appendChild(messageText);
    senderDiv.appendChild(cardDiv);
    messageDiv.appendChild(senderDiv);

    messageContainer.appendChild(messageDiv);

    // Ajusta o scroll para a última mensagem
    messageContainer.scrollTop = messageContainer.scrollHeight;

    // Verifica se há mensagens no container
    checkMessages();
  }

  function checkMessages() {
    if (messageContainer.children.length > 0) {
      welcomeMessage.style.display = "none";
      messageContainer.style.display = "flex";
    } else {
      welcomeMessage.style.display = "flex";
      messageContainer.style.display = "none";
    }
  }

  sendButton.addEventListener("click", () => {
    const userMessage = textarea.value.trim();

    // Desliga o microfone se estiver ligado
    if (btnParar.style.display === "block") {
      btnParar.style.display = "none";
      btnGravar.style.display = "block";
      speech.stop();
    }

    if (userMessage) {
      createMessage(userMessage, "message-person");

      textarea.value = "";

      setTimeout(() => {
        createMessage(`Recebi sua mensagem: "${userMessage}"`, "message-boot");
      }, 1000);
    }
  });

  // Verifica o estado ao carregar a página
  window.addEventListener("load", checkMessages);
});
