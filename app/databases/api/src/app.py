from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # noqa

from .routes import products, users

from .clients.sqlite import create_db_and_tables
create_db_and_tables()


app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
