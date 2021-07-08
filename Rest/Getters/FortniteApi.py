import httpx
import json

from typing import Union, List

from Rest.Models.FortniteApi import Cosmetic, NewCosmetics, Build, NewsV2, ShopV2


class FortniteApi:
    def __init__(self, data):
        self.http = httpx
        self.language = data.language
        self.key = data.key[0]

        self.headers = {
            'x-api-key': self.key
        }

        self.params = {
            'language': self.language
        }

    def new_cosmetics(self) -> Union[None, NewCosmetics]:
        res = self.http.get(
            url='https://fortnite-api.com/v2/cosmetics/br/new',
            headers=self.headers,
            params=self.params
        )
        if res.status_code == 200:
            data = res.json()['data']
            return NewCosmetics(data)

    def get_build(self) -> Union[None, Build]:
        res = self.http.get(
            url='https://fortnite-api.com/v2/aes',
            headers=self.headers
        )
        if res.status_code == 200:
            data = res.json()['data']
            return Build(data)

    def search_cosmetic(self, cosmetic: str = None, pak_id: Union[str, int] = None) -> Union[None, List[Cosmetic]]:
        if cosmetic:
            self.params.update(name=cosmetic)
            self.params.update(matchMethod='contains')
        elif pak_id:
            self.params.update(dynamicPakId=pak_id)

        res = self.http.get(
            url="https://fortnite-api.com/v2/cosmetics/br/search/all",
            headers=self.headers,
            params=self.params
        )

        if res.status_code == 200:
            data = res.json()['data']
            return [Cosmetic(i) for i in data]

    def get_shop(self):
        res = self.http.get(
            url="https://fortnite-api.com/v2/shop/br/combined",
            headers=self.headers,
            params=self.params
        )

        if res.status_code == 200:
            data = res.json()['data']
            return ShopV2(data)

    def get_news(self):
        res = self.http.get(
            url="https://fortnite-api.com/v2/news/br",
            headers=self.headers,
            params=self.params
        )

        if res.status_code == 200:
            data = res.json()['data']
            return NewsV2(data)
    
    def shop_sections(self):
        res = self.http.get(
            url="http://api.fn-utility.tk:2131/api/v1/shopsection",
            params=self.params
        )

        if res.status_code == 200:
            data = res.json()['data']
            return data