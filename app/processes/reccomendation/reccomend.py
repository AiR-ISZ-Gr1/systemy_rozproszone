import requests
import numpy as np
from fastapi import FastAPI, HTTPException

app = FastAPI()
url = 'http://api:8000/products'

@app.get('/get_reccomendations/{number}')
def get_reccomendations(number: int):
    try:
        documents = requests.get(url).json()
        profit = [item.get('sell_price') - item.get('buy_price') for item in documents if item.get('is_enabled')]
        if profit:
            profit = np.array(profit)/max(profit)*2/3
            quantites = [item.get('quantity') for item in documents]
            quantites = np.array(quantites)/max(quantites)*1/3
            score = profit+quantites
            names = [{"id":item.get('id'), "score":sc} for item,sc in zip(documents,score)]
            sorted_data = sorted(names, key=lambda x: x['score'], reverse=True)
            products = [requests.get(f'{url}/{item["id"]}').json() for item in sorted_data[:number]]
        else:
            products =[]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))