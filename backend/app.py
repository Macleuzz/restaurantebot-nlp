from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import RestauranteBot
import config

settings = BotFrameworkAdapterSettings(
    config.MicrosoftAppId,
    config.MicrosoftAppPassword
)
adapter = BotFrameworkAdapter(settings)
bot     = RestauranteBot()

async def messages(req: web.Request) -> web.Response:
    body     = await req.json()
    activity = Activity().deserialize(body)
    auth     = req.headers.get("Authorization", "")

    async def callback(turn_context):
        await bot.on_turn(turn_context)

    await adapter.process_activity(activity, auth, callback)
    return web.Response(status=200)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3978)