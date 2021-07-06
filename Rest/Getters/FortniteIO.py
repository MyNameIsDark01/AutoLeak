import httpx

from typing import List, Union
from colorama import Fore
from getch import pause

from Rest.Models.FortniteIO import Weapon


class FortniteIO:
    def __init__(self, data):
        self.http = httpx
        self.language = data.language
        self.key = data.key[1]

        self.params = {
            'language': self.language
        }
        self.headers = {
            'authorization': self.key
        }

    def search_weapon(self, weapon_name: str = None, weapon_id: str = None) -> Union[None, List[Weapon]]:
        if weapon_id:
            self.params.update(id=weapon_id)
        elif weapon_name:
            self.params.update(name=weapon_name)

        res = self.http.get(
            url="https://fortniteapi.io/v1/loot/list",
            headers=self.headers,
            params=self.params
        )
        if res.status_code == 200:
            data = res.json()
            if data['result']:
                data = res.json()['weapons']
                if len(data) > 0:
                    return [Weapon(i) for i in data]
            elif data['code'] == ['MISSING_API_KEY', 'INVALID_API_KEY']:
                exit(pause(Fore.RED + "API Key isn't defined or isn't valid."))
