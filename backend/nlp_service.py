import aiohttp
import config

async def analizar(texto: str):
    url = (f"{config.LANGUAGE_ENDPOINT}language/:analyze-conversations"
           f"?api-version=2024-11-15-preview")
    headers = {
        "Ocp-Apim-Subscription-Key": config.LANGUAGE_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "user",
                "text": texto
            }
        },
        "parameters": {
            "projectName":    config.LANGUAGE_PROJECT,
            "deploymentName": config.LANGUAGE_DEPLOYMENT
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as resp:
            data = await resp.json()

    if "result" not in data:
        print(f"Error Azure: {data}")
        return "None", {}, 0.0

    resultado = data["result"]["prediction"]
    intencion = resultado["topIntent"]
    confianza = resultado["intents"][0]["confidenceScore"]
    entidades = {}
    for e in resultado.get("entities", []):
        entidades[e["category"]] = e["text"]

    return intencion, entidades, confianza