import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

async def test():
    url = (f"{os.getenv('LANGUAGE_ENDPOINT')}language/:analyze-conversations"
           f"?api-version=2024-11-15-preview")
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("LANGUAGE_KEY"),
        "Content-Type": "application/json"
    }
    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "user",
                "text": "Quiero reservar una mesa para 4 el viernes"
            }
        },
        "parameters": {
            "projectName":    os.getenv("LANGUAGE_PROJECT"),
            "deploymentName": os.getenv("LANGUAGE_DEPLOYMENT")
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as resp:
            data = await resp.json()
            print("=== RESPUESTA COMPLETA DE AZURE ===")
            print(data)
            print("===================================")
            
            if "result" in data:
                resultado = data["result"]["prediction"]
                print(f"✅ Intención detectada: {resultado['topIntent']}")
                print(f"📦 Entidades: {[e['text'] for e in resultado.get('entities',[])]}")
            else:
                print("❌ Error:", data)

asyncio.run(test())