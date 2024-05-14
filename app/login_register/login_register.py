from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from passlib.context import CryptContext

app = FastAPI()
base_url = "http://api:8000/users"

# Kontekst do hashowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class Login(BaseModel):
    username: str
    password: str

# Endpoint do rejestracji użytkownika
@app.post("/register/")
def register_user(user: User):
    # Hashuj hasło przed zapisaniem
    response = requests.get(base_url, params={"username": user.username})
    if response.json():
        # Jeśli lista nie jest pusta, użytkownik już istnieje
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    response = requests.post(base_url, json=user.dict())
    return response.json()


# Endpoint do logowania użytkownika
@app.post("/login/")
def login_user(login: Login):
    response = requests.get(base_url, params={"username": login.username})
    user_data = response.json()
    if user_data and pwd_context.verify(login.password, user_data[0]['password']):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")