import httpx


class FortniteIO:
    def __init__(self, data):
        self.http = httpx
        self.language = data.language
        self.key = data.key[1]

        self.headers = {
            'language': self.language,
            'authorization': self.key
        }
