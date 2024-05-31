from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import pandas as pd
import os
import requests

def create_user(username, password, is_admin=False):
    user_data = {
        "username": username,
        "password": password,
        "is_admin": is_admin
    }
    response = requests.post("http://api:8000/users/register/", json=user_data)
    return response.json()

def create_products(data):
    base_url = "http://api:8000"
    for _,item in data.iterrows():
        product_data = {
        "id": item['id'],
        "name": item['Name'][0] + item['Name'][1:].lower(),
        "description": item['Description'],
        "sale_price": item['Sale_price'],
        "quantity": item['Quantities'],
        "buy_price": item['Buy_price'],
        "date": 'None',
        "picture_path": item['pic_path']
        }
        response = requests.post(f"{base_url}/products/", json=product_data)
        print(response.json())

def process_data(data, qdrant_url: str):
    model = SentenceTransformer('intfloat/e5-small-v2')
    vec_len = model[1].word_embedding_dimension
    client = QdrantClient(url=qdrant_url)
    names = [item.name for item in client.get_collections().collections]
    
    if 'products_description' not in names:
        client.create_collection(
            collection_name="products_description",
            vectors_config=VectorParams(size=vec_len, distance=Distance.COSINE),
        )
    else:
        print('Collection exists')

    points = [PointStruct(
                    id=index,
                    vector=model.encode(item['Description'], normalize_embeddings=True),
                    payload={"Id": item['id'], "Name": item['Name'], "Description": item['Description']}
                ) for index, item in data.iterrows()]

    operation_info = client.upsert(
        collection_name="products_description",
        wait=True,
        points=points,
    )
    print(operation_info)

def main():
    data_path = 'init_data/products/flowershopdata_clean.csv'
    data = pd.read_csv(data_path)
    qdrant_url = "http://qdrant:6333"
    process_data(data, qdrant_url)
    create_products(data)
    create_user('TestA','!234qwer',1)
    create_user('TestU','!234qwer',0)

if __name__ == "__main__":
    main()
