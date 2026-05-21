function activarVoz() {
    const btn = document.getElementById("btn-mic");

    if (!('webkitSpeechRecognition' in window ||
          'SpeechRecognition' in window)) {
        alert("Tu navegador no soporta reconocimiento de voz. Usa Chrome.");
        return;
    }

    const recognition = new (window.SpeechRecognition ||
                              window.webkitSpeechRecognition)();
    recognition.lang = "es-PE";
    recognition.continuous = false;
    recognition.interimResults = false;

    btn.textContent = "🔴";
    recognition.start();

    recognition.onresult = (event) => {
        const texto = event.results[0][0].transcript;
        document.getElementById("input").value = texto;
        btn.textContent = "🎤";
        enviar();
    };

    recognition.onerror = () => {
        btn.textContent = "🎤";
        alert("No se pudo escuchar. Intenta de nuevo.");
    };

    recognition.onend = () => {
        btn.textContent = "🎤";
    };
}