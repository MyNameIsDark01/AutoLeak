import httpx

from Rest.Models.FortniteApi import NewCosmetics, Build


class FortniteApi:
    def __init__(self, data):
        self.http = httpx
        self.language = data.language
        self.key = data.key[0]

        self.headers = {
            'language': self.language,
            'authorization': self.key
        }

    def new_cosmetics(self):
        res = self.http.get(
            url='https://fortnite-api.com/v2/cosmetics/br/new',
            headers=self.headers
        )
        if res.status_code == 200:
            data = res.json()['data']
            return NewCosmetics(data)

    def get_build(self):
        res = self.http.get(
            url='https://fortnite-api.com/v2/aes'
        )
        if res.status_code == 200:
            data = res.json()['data']
            return Build(data)