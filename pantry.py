import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

class Pantry:
    
    def __init__(self):
        self.id = os.getenv('PANTRY_ID')
        url = f"https://getpantry.cloud/apiv1/pantry/{self.id}/basket/"

    def get(self, basket_name: str):

        payload = ""
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", self.url + basket_name, headers=headers, data=payload)

        return response.json()

    def put(self, basket_name: str, data: dict):
        payload = json.dumps(data)
    
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", self.url + basket_name, headers=headers, data=payload)

        return response.json()
