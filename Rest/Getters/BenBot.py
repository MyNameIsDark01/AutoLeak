import httpx
import json

from typing import Union, List

from Rest.Models.BenBot import NewCosmetics, Build


BASE_URL = "https://benbot.app/api/"

class BenBot:
    def __init__(self, data):
        self.http = httpx.Client()
        self.language = data.language

        self.params = {
            'lang': self.language
        }

    def new_cosmetics(self) -> Union[None, NewCosmetics]:
        res = self.http.get(
            url=BASE_URL + 'v1/newCosmetics',
            params=self.params
        )
        if res.status_code == 200:
            data = res.json()
            return NewCosmetics(data)
    
    def get_build(self) -> Union[None, Build]:
        res = self.http.get(
            url=BASE_URL + 'v1/aes',
        )
        if res.status_code == 200:
            data = res.json()
            return Build(data)