from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import pandas as pd
import os
import requests
import nanoid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from io import BytesIO
from PIL import Image


image_download_url = "http://api:8000/files/download/"
image_upload_url = "http://api:8000/files/upload"


class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)
    
    def show_photo(self):
        response = requests.get(f"{image_download_url}{self.image_id}", stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None

    # Function to compress image
    @staticmethod
    def compress_image(img: Image.Image, output_size=(320, 320), quality=70) -> BytesIO:
        img.thumbnail(output_size)
        output = BytesIO()
        img.save(output, format='PNG', quality=quality)
        output.seek(0)
        return output

    # Function to add product image
    def add_product_image(self, file):
        img = self.compress_image(Image.open(file))
        img_extension = file.split('.')[-1]
        files = {'file': (f'{self.date}_{self.name}.{img_extension}', img, f'image/{img_extension}')}
        response = requests.post(image_upload_url, files=files)
        response.raise_for_status()  # Check for request errors
        self.image_id = response.json().get('file_id')
        return response

def create_user(username, password,address,cart, is_admin=False):
    user_data = {
        "username": username,
        "password": password,
        "is_admin": is_admin,
    }
    resp = requests.get("http://api:8000/users/").json()
    all_users = [user.get('username') for user in resp]
    if username not in all_users:
        response = requests.post("http://api:8000/users/", json=user_data)
        return response.json()
    else:
        print("user with this name exists")

def init_qdrant(data, qdrant_url: str):
    vec_len = 384 #lenght of vector for embedding model
    client = QdrantClient(url=qdrant_url)
    names = [item.name for item in client.get_collections().collections]
    
    if 'products_description' not in names:
        client.create_collection(
            collection_name="products_description",
            vectors_config=VectorParams(size=vec_len, distance=Distance.COSINE),
        )
    else:
        print('Collection exists')


def main():
    data_path = 'init_data/products/flowershopdata_clean.csv'
    data = pd.read_csv(data_path)

    qdrant_url = "http://qdrant:6333"
    init_qdrant(data, qdrant_url)
    
    for _,item in data.iterrows():
        product = Product(
        id =  item['id'],
        name= item['Name'][0] + item['Name'][1:].lower(),
        description= item['Description'],
        sell_price= item['Sale_price'],
        quantity= item['Quantities'],
        buy_price= item['Buy_price'],
        date= 'None',
        tags= [item['tags']]
        )
        response = requests.get(f'http://api:8000/products/name/{product.name}')
        if response.status_code == 200:
            print('Product exists')
        else:
            product.add_product_image(item['pic_path'])
            response = requests.post(f'http://api:8000/products/', json=product.dict())
            if response.status_code == 200:
                print('Product created')

    
    create_user('TestA','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',1,1,1)
    create_user('TestU','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0,0,0)

if __name__ == "__main__":
    main()
