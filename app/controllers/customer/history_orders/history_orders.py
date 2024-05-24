from fastapi import FastAPI, HTTPException, Request
import csv
import os

app = FastAPI()

# Mockowa baza danych zamówień z nazwami użytkowników
orders_database = {
    "12347777": [
        {"order_id": 1, "status": "Dostarczone", "products": [
            {"name": "Laptop", "price": 1500, "review": True},
            {"name": "Mouse", "price": 50, "review": False}
        ]},
        {"order_id": 2, "status": "W trakcie realizacji", "products": [
            {"name": "Smartphone", "price": 800, "review": False},
            {"name": "Charger", "price": 20, "review": False}
        ]}
    ]
}

# Endpoint do pobierania historii zamówień
@app.get("/orders/{username}")
async def get_order_history(username: str):
    if username in orders_database:
        return orders_database[username]
    else:
        raise HTTPException(status_code=404, detail="Orders not found")

# Endpoint do przyjmowania opinii o produktach
@app.post("/review")
async def submit_review(request: Request):
    review = await request.json()
    username = review.get("username")
    order_id = review.get("order_id")
    product = review.get("product")
    review_text = review.get("review")
    
    if not username or not order_id or not product or not review_text:
        raise HTTPException(status_code=400, detail="Incomplete review data")

    review_filename = "reviews.csv"
    review_exists = os.path.isfile(review_filename)

    with open(review_filename, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not review_exists:
            writer.writerow(["username", "order_id", "product", "review"])
        writer.writerow([username, order_id, product, review_text])

    return {"message": "Review submitted successfully"}
