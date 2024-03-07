from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb+srv://spambartosz123:c0WDL8nciXDSAo1w@cluster0.ffekdag.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['systemy_rozproszone2']
collection = db["users"]

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    user_data = user.dict()
    username = user_data.get('username')
    password = user_data.get('password')
    if username and password:
        if collection.find_one({'username': username}):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'message': 'User already exists.'})
        
        hash_pass = generate_password_hash(password)
        collection.insert_one({'username': username, 'password': hash_pass})
        return {'message': 'User registered successfully.'}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing username or password.")

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: User):
    user_data = user.dict()
    username = user_data.get('username')
    password = user_data.get('password')
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing username or password.")
    
    user = collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return {'message': 'Logged in successfully.'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")

