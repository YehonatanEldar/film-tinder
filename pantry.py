import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

class Pantry:
    
    def __init__(self):
        self.id = os.getenv('PANTRY_ID')
        self.url = f"https://getpantry.cloud/apiv1/pantry/{self.id}"

    def base_func(self, action: str, data: dict | None, url: str):
        time.sleep(0.6)
        if data:
            payload = json.dumps(data)
        else:
            payload = ''


        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request(action, url, headers=headers, data=payload)

        try:

            return response.json()
        
        except requests.exceptions.JSONDecodeError:
            return response.text


    def get_data(self):

        return self.base_func("GET", None, self.url)

    def get(self, basket_name: str):
        new_url = f'{self.url}/basket/{basket_name}'

        return self.base_func("GET", None, new_url)

    def put(self, basket_name: str, data: dict):
        new_url = f'{self.url}/basket/{basket_name}'
        
        return self.base_func("PUT", data, new_url)
    
    def new_basket(self, basket_name: str, data: dict):
        new_url = f'{self.url}/basket/{basket_name}'
        
        return self.base_func("POST", data, new_url)
    
    def delete_basket(self, basket_name):
        new_url = f'{self.url}/basket/{basket_name}'
        return self.base_func("DELETE", None, new_url)
    
    def delete_all_baskets(self):
        data = self.get_data()
        basket_list = [d['name'] for d in data['baskets']]

        for name in basket_list:
            self.delete_basket(name)


