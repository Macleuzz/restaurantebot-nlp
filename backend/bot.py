from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
import nlp_service, db_service
from menu_data import MENU, INFO

class RestauranteBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        texto   = turn_context.activity.text.strip()
        usuario = turn_context.activity.from_property.name or "Cliente"

        intencion, entidades, confianza = await nlp_service.analizar(texto)

        if intencion == "ReservarMesa":
            respuesta = await self.reservar_mesa(entidades, usuario)

        elif intencion == "ConsultarMenu":
            respuesta = self.consultar_menu(entidades)

        elif intencion == "HacerPedido":
            respuesta = self.hacer_pedido(entidades, usuario)

        elif intencion == "EstadoPedido":
            respuesta = self.estado_pedido(entidades, usuario)

        elif intencion == "ContactarRestaurante":
            respuesta = self.contactar()

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
        await turn_context.send_activity(MessageFactory.text(respuesta))

    # ── ReservarMesa ──
    async def reservar_mesa(self, entidades, usuario):
        fecha      = entidades.get("fecha")
        hora       = entidades.get("hora")
        num_p      = entidades.get("num_personas")

        if not fecha:
            return "📅 ¿Para qué fecha deseas la reserva? (Ej: el viernes 20 de junio)"
        if not hora:
            return f"🕐 ¿A qué hora deseas la mesa el {fecha}?"
        if not num_p:
            return "👥 ¿Para cuántas personas es la reserva?"

        id_r = db_service.crear_reserva(usuario, fecha, hora, num_p)
        return (
            f"✅ ¡Reserva confirmada!\n"
            f"📅 Fecha: {fecha}\n"
            f"🕐 Hora: {hora}\n"
            f"👥 Personas: {num_p}\n"
            f"🔖 Código: #{id_r}\n"
            f"Te esperamos en La Huaca Dorada 🍽️"
        )

    # ── ConsultarMenu ──
    def consultar_menu(self, entidades):
        categoria = entidades.get("categoria_menu")
        plato     = entidades.get("nombre_plato")

        try:
            filas = db_service.obtener_menu(categoria or plato)
            if not filas:
                raise Exception("vacío")
            if categoria or plato:
                resp = f"🍽️ Resultados para '{categoria or plato}':\n\n"
                for f in filas:
                    resp += f"• {f[0]} — S/ {f[1]:.2f}\n"
            else:
                resp = "📋 Nuestro menú completo:\n\n"
                cat_actual = ""
                for f in filas:
                    if f[0] != cat_actual:
                        cat_actual = f[0]
                        resp += f"\n🔸 {cat_actual}\n"
                    resp += f"  • {f[1]} — S/ {f[2]:.2f}\n"
        except:
            resp = "📋 Nuestro menú:\n\n"
            for cat, platos in MENU.items():
                resp += f"\n🔸 {cat}\n"
                for p in platos:
                    resp += f"  • {p['nombre']} — S/ {p['precio']:.2f}\n"
        return resp

    # ── HacerPedido ──
    def hacer_pedido(self, entidades, usuario):
        plato = entidades.get("nombre_plato")
        if not plato:
            return "🍽️ ¿Qué deseas ordenar? Dime el nombre del plato."

        id_p = db_service.crear_pedido(usuario, plato)
        return (
            f"✅ ¡Pedido registrado!\n"
            f"🍽️ Plato: {plato}\n"
            f"📦 Número de pedido: #{id_p}\n"
            f"⏱️ Tiempo estimado: 30-45 minutos\n"
            f"Puedes consultar el estado con tu número de pedido."
        )

    # ── EstadoPedido ──
    def estado_pedido(self, entidades, usuario):
        id_p   = entidades.get("id_pedido")
        nombre = usuario

        fila = db_service.estado_pedido(id_p, nombre)
        if not fila:
            return "❌ No encontré tu pedido. ¿Puedes darme el número de pedido?"

        return (
            f"📦 Estado de tu pedido #{fila[0]}:\n"
            f"🍽️ Detalle: {fila[1]}\n"
            f"📊 Estado: {fila[2]}\n"
            f"🕐 Hora de pedido: {fila[3].strftime('%H:%M')}"
        )

    # ── ContactarRestaurante ──
    def contactar(self):
        return (
            f"📞 Información de La Huaca Dorada:\n\n"
            f"📍 {INFO['direccion']}\n"
            f"☎️ {INFO['telefono']}\n"
            f"📧 {INFO['email']}\n"
            f"🕐 {INFO['horario']}\n\n"
            f"¡Con gusto te atendemos!"
        )

    async def on_members_added_activity(self, members_added, turn_context):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 ¡Bienvenido a La Huaca Dorada!\n\n"
                    "Soy tu asistente virtual. Puedo ayudarte con:\n"
                    "🍽️ Reservar una mesa\n"
                    "📋 Ver el menú\n"
                    "🛵 Hacer un pedido\n"
                    "📦 Estado de tu pedido\n"
                    "📞 Información de contacto\n\n"
                    "¿En qué te puedo ayudar?"
                )