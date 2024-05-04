from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class Number(BaseModel):
    value: int

@app.get("/echo_number/")
async def echo_number(number: int = Query(default=1, description="Number to echo back")):
    return {"received_number": number}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
