from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot import RestauranteBot
import db_service
import config
import json

settings = BotFrameworkAdapterSettings(
    config.MicrosoftAppId,
    config.MicrosoftAppPassword
)
adapter = BotFrameworkAdapter(settings)
bot = RestauranteBot()

# ── CORS headers ──
def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

# ── Preflight OPTIONS ──
async def options_handler(req: web.Request) -> web.Response:
    return web.Response(status=200, headers=cors_headers())

# ── Ruta del chat (simplificada) ──
async def chat(req: web.Request) -> web.Response:
    try:
        body    = await req.json()
        texto   = body.get("text", "")
        usuario = body.get("usuario", "Cliente")

        # Procesar con el bot directamente
        import nlp_service, asyncio
        intencion, entidades, confianza = await nlp_service.analizar(texto)

        bot_instance = RestauranteBot()
        
        if intencion == "ReservarMesa":
            respuesta = await bot_instance.reservar_mesa(entidades, usuario)
        elif intencion == "ConsultarMenu":
            respuesta = bot_instance.consultar_menu(entidades)
        elif intencion == "HacerPedido":
            respuesta = bot_instance.hacer_pedido(entidades, usuario)
        elif intencion == "EstadoPedido":
            respuesta = bot_instance.estado_pedido(entidades, usuario)
        elif intencion == "ContactarRestaurante":
            respuesta = bot_instance.contactar()
        else:
            respuesta = (
                "No entendí tu consulta 😊 Puedo ayudarte con:\n"
                "🍽️ Reservar una mesa\n"
                "📋 Ver el menú\n"
                "🛵 Hacer un pedido\n"
                "📦 Estado de tu pedido\n"
                "📞 Contactar con nosotros"
            )

        db_service.guardar_conversacion(
            usuario, texto, intencion, confianza, respuesta
        )

        return web.Response(
            text=json.dumps({"text": respuesta}, ensure_ascii=False),
            content_type="application/json",
            headers=cors_headers()
        )
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(
            text=json.dumps({"text": f"Error interno: {str(e)}"}),
            content_type="application/json",
            headers=cors_headers()
        )

# ── Ruta historial ──
async def historial(req: web.Request) -> web.Response:
    inicio = req.rel_url.query.get("inicio", "2024-01-01T00:00")
    fin    = req.rel_url.query.get("fin",    "2099-12-31T23:59")
    data   = db_service.historial(inicio, fin)
    return web.Response(
        text=json.dumps(data, ensure_ascii=False),
        content_type="application/json",
        headers=cors_headers()
    )

# ── Ruta estadísticas ──
async def estadisticas(req: web.Request) -> web.Response:
    filas = db_service.estadisticas()
    data  = [{"intencion": f[0], "total": f[1]} for f in filas]
    return web.Response(
        text=json.dumps(data, ensure_ascii=False),
        content_type="application/json",
        headers=cors_headers()
    )

app = web.Application()
app.router.add_post("/api/chat",          chat)
app.router.add_options("/api/chat",       options_handler)
app.router.add_get("/api/historial",      historial)
app.router.add_options("/api/historial",  options_handler)
app.router.add_get("/api/estadisticas",   estadisticas)
app.router.add_options("/api/estadisticas", options_handler)

if __name__ == "__main__":
    print("🍽️  RestauranteBot corriendo en http://localhost:3978")
    web.run_app(app, host="0.0.0.0", port=3978)