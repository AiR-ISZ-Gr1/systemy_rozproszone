from fastapi import FastAPI, HTTPException

app = FastAPI()

# Mockowa baza danych zamówień z nazwami użytkowników
orders_database = {
    "sample_user": [
        {"order_id": 1, "product": "Laptop", "price": 1500, "status": "Przyjęte"},
        {"order_id": 2, "product": "Smartphone", "price": 800, "status": "W trakcie realizacji"},
    ],
    "user2": [
        {"order_id": 3, "product": "Słuchawki", "price": 200, "status": "Dostarczone"},
    ]
}

# Endpoint do pobierania historii zamówień
@app.get("/orders/{username}")
async def get_order_history(username: str):
    if username in orders_database:
        return orders_database[username]
    else:
        raise HTTPException(status_code=404, detail="Orders not found")

