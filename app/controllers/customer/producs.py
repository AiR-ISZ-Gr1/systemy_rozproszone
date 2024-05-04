from fastapi import FastAPI
import random
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Produkt(BaseModel):
    nazwa: str
    zdjecie: str
    cena: str
    opis: str

@app.get("/produkty/", response_model=List)
async def generuj_produkty(N: int) -> List:
    produkty = []
    for i in range(1, N + 1):
        cena = "${:.2f}".format(random.uniform(5, 50))  # Losowa cena w przedziale od $5.00 do $50.00
        nazwa = f"Produkt {i}"
        opis = f"To jest opis {nazwa}"
        produkt = Produkt(nazwa=nazwa, zdjecie="test.jpg", cena=cena, opis=opis)
        produkty.append(produkt)
    return {"products", produkty}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

