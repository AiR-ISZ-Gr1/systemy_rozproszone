from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from dataclasses_custom.chatbot_class import Chatbot
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("intfloat/e5-small-v2")
bot = Chatbot(data = {
    "openai_client":  AsyncOpenAI(api_key="sk-proj-8j1NyU5gvA4njucbGG3uT3BlbkFJxBLHcRn4z7futfYb4sgb")
}, embedding_model= model)

@app.get("/ask/{question}")
async def answer(question: str):
    try:
        result = await bot.answer(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
