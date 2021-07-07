import time
import os
import json
import datetime

from colorama import Fore

from Rest.Models.FortniteApi import ShopV2
from Utilities.ShopGenerator import ShopGenerator


class ShopUpdate:
    def __init__(self, data):
        self.api = data.api[0]
        self.language = data.language

        self.delay = data.delay

        self.twitter = data.twitter
        self.tweetShop = data.tweetShop
        self.text = data.shopText

    def main(self):
        count = 1

        while True:
            print(Fore.YELLOW + f'Checking for changes: -> [{count}]')
            res = self.api.get_shop()
            if not res:
                time.sleep(self.delay)
                continue

            if not os.path.isfile('Cache/shop.json'):
                open('Cache/shop.json', 'w+').write(res.json())
                time.sleep(self.delay)
                continue

            old_shop = ShopV2(json.loads(open('Cache/shop.json').read()))
            if res.hash != old_shop.hash:
                print(Fore.GREEN + "Shop changed, generating now...")
                open('Cache/shop.json', 'w+').write(res.json())

                self.create_shop(res)
                if self.tweetShop:
                    self.tweet_shop()
            
            time.sleep(self.delay)
            count += 1

    def create_shop(self, item_shop = None):
        if not item_shop:
            item_shop = self.api.get_shop()
        
        generateshop = ShopGenerator(self)
        generateshop.generateImage(item_shop)

    def tweet_shop(self):
        date = datetime.datetime.utcnow().strftime('%d %B %Y')
        text = self.text

        try:
            self.twitter.update_with_media(
                "Cache/itemshop.jpg",
                status=text.format(date=date)
            )
            print(Fore.GREEN + f"Tweeted current shop image.")
        except Exception as e:
            print(Fore.RED + f"Failed to tweet shop image [{e}]")