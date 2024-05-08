from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # noqa

from models.address import *
from models.cart import *
from models.order import *
from models.product import *
from models.user import *

from routes import (
    products,
    orders,
    users,
    carts,
    addresses,
)

from clients.postgres import init_db
init_db()


app = FastAPI()

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(users.router)
app.include_router(carts.router)
app.include_router(addresses.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
