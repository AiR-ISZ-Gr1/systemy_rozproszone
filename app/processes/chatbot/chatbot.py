from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from dataclasses_custom.chatbot_class import Chatbot, PromptFiller
import os
import httpx

app = FastAPI()

# Create a clean http client without proxy settings
http_client = httpx.AsyncClient()

# Initialize OpenAI client with explicit http client
openai_client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    http_client=http_client
)

bot = Chatbot(data={"openai_client": openai_client})
filler = PromptFiller()

@app.get("/ask/{question}")
async def answer(question: str):
    try:
        system, user = await filler.prepare_question(question)
        print(f'{system} ----- {user}')
        return StreamingResponse(
            bot.answer(system, user),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask/names/{question}")
async def get_names(question: str):
    try:
        flowers = [flower.get('Name') for flower in await filler.get_names(question)]
        print(f'flowers: {flowers}\n')
        return flowers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()