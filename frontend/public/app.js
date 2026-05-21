const API_URL = "http://localhost:3978/api/chat";

window.onload = () => {
    agregarMensaje("bot",
        "👋 ¡Bienvenido a La Huaca Dorada!\n\n" +
        "Puedo ayudarte con:\n" +
        "🍽️ Reservar una mesa\n" +
        "📋 Ver el menú\n" +
        "🛵 Hacer un pedido\n" +
        "📦 Estado de tu pedido\n" +
        "📞 Información de contacto\n\n" +
        "¿En qué te puedo ayudar?"
    );
};

async function enviar() {
    const input = document.getElementById("input");
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje("usuario", texto);
    input.value = "";
    mostrarTyping(true);

    try {
        const resp = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: texto,
                usuario: "Cliente"
            })
        });

        const data = await resp.json();
        mostrarTyping(false);
        agregarMensaje("bot", data.text);

    } catch (e) {
        mostrarTyping(false);
        agregarMensaje("bot", "⚠️ Error al conectar con el servidor.");
        console.error(e);
    }
}

function agregarMensaje(tipo, texto) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = `burbuja ${tipo}`;
    div.textContent = texto;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function mostrarTyping(mostrar) {
    document.getElementById("typing").style.display =
        mostrar ? "flex" : "none";
}