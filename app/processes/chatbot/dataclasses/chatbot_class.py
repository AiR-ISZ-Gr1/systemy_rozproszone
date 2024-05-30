from qdrant_client import QdrantClient, models
from pymongo import MongoClient
from qdrant_client import QdrantClient
from openai import OpenAI
from typing import List
from sentence_transformers import SentenceTransformer

class Chatbot():
    mongo_client: MongoClient
    qdrant_client: QdrantClient
    openai_client: OpenAI
    embedding_model: str

    def __init__(self, **data):
        self.mongo_client = data.pop('mongo_client', None)
        self.qdrant_client = data.pop('qdrant_client', None)
        self.openai_client = data.pop('openai_client', None)
        self.embedding_model = SentenceTransformer(data.pop('embedding_model', None))

    def answer(self,question:str) -> str:
        system,user = self.__prepare_question(question)
        chat_completion = self.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system", "content" : system},
            {"role": "user", "content": user}])
        
        return chat_completion.choices[0].message.content


    def __fill_prompt(self,question:str, jsons:List[str]) -> List[str]:
        SYSTEM_TEMPLATE = """You are a professional flower shop assistatnt, you reccomend products that fullfils
        every user expectations or answer his question based only on data in json format below:
        {}
        Always check the quantity before recommending if it's equal to 0 ask to wait until restock.
        If none of products fulfill expectations say that sadly we don't have product you need.
        Your answer should short and contain only what flower you recommend, reasoning why and friendly insight.
        Don't encourage further conversation.
        """

        filled_prompt = SYSTEM_TEMPLATE.format(jsons)
        return filled_prompt, question


    def __qdrant_search(self, question:str):
        query = self.embedding_model.encode(question, normalize_embeddings=True)
        results = self.qdrant_client.search(
            collection_name="products_description",
            query_vector=query,
            limit=3,
        )
        return results


    def __search_mongo(self, results):
        db = self.mongo_client["ecommerce-app"]
        collection = db['products']
        all_jsons = []
        for flower_id in [res.payload.get('Id') for res in results]:
            json_data = {}
            for item in collection.find({"id":flower_id}):
                json_data['Name'] = item.get('name')
                json_data['Description'] = item.get('description')
                json_data['Quantity'] = item.get('quantity')
                all_jsons.append(json_data)
        return all_jsons


    def __prepare_question(self, question):
        qdrant_result = self.__qdrant_search(question)
        mongo_result = self.__search_mongo(qdrant_result)
        return self.__fill_prompt(question,mongo_result)
    