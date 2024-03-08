import os
from dotenv import load_dotenv

load_dotenv('../.env')

def get_variable(variable_name: str):
    return os.getenv(variable_name)