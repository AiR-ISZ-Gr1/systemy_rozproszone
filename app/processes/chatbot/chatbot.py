from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from dataclasses_custom.chatbot_class import Chatbot, PromptFiller

app = FastAPI()
bot = Chatbot(data = {
    "openai_client":  AsyncOpenAI(api_key="sk-proj-8j1NyU5gvA4njucbGG3uT3BlbkFJxBLHcRn4z7futfYb4sgb")
})
filler = PromptFiller()

@app.get("/ask/{question}")
async def answer(question: str):
    try:
        system,user = await filler.prepare_question(question)
        return StreamingResponse(bot.answer(system,user), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
