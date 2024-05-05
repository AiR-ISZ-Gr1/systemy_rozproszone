from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # noqa

from .routes import products


app = FastAPI()

app.include_router(products.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
