import time
import os
import json

from colorama import Fore


class ShopSection:
    def __init__(self, data):
        self.name = data.name
        self.api = data.api[0]
        self.delay = data.delay

        self.twitter = data.twitter
        self.tweetSection = data.tweetSection
        self.text = data.shopSectionText

    def main(self):
        count = 1

        while True:
            print(Fore.YELLOW + f"Checking for changes: -> [{count}]")
            res = self.api.shop_sections()
            if not res:
                time.sleep(self.delay)
                continue

            if not os.path.isfile("Cache/section.json"):
                open("Cache/section.json", "w+").write(json.dumps(res))

            old = json.loads(open("Cache/section.json").read())

            if res[-1]['hash'] != old[-1]['hash']:
                print(Fore.GREEN + "Shop sections changed!")
                open("Cache/section.json", "w+").write(json.dumps(res))

                if self.tweetSection:
                    self.tweet_section(res[-1]['shop'])
            
            count += 1
            time.sleep(self.delay)

    def tweet_section(self, data):
        name = self.name
        text = self.text

        sections = ""

        for i in data:
            sections += f"{i['sectionName']} - {i['quantity']}\n"

        try:
            self.twitter.update_status(
                status=text.format(sections=sections, name=name)
            )
            print(Fore.GREEN + 'Tweeted shop sections!')
        except Exception as e:
            print(Fore.RED + f"Failed to tweet shop sections [{e}]")