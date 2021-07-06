import requests
import time
import os
import json
import datetime

from colorama import Fore

from Rest.Models.FortniteApi import NewsV2
from Utilities.NewsGenerator import NewsGenerator


class News:
    def __init__(self, data):
        self.name = data.name

        self.api = data.api[0]
        self.language = data.language
        self.delay = data.delay

        self.twitter = data.twitter
        self.tweetNews = data.tweetNews

        self.feed = ""
        self.date = ""
    
    def main(self):
        count = 1

        while True:
            print(f"Checking for changes in news feed: -> [{count}]")
            res = self.api.get_news()
            if not res:
                time.sleep(self.delay)
                continue
            
            if not os.path.isfile('Cache/news.json'):
                open('Cache/news.json', 'w+').write(res.json())

            old_news = NewsV2(json.loads(open('Cache/news.json').read()))

            if res.hash != old_news.hash:
                open('Cache/news.json', 'w+').write(res.json())

                self.date = datetime.datetime.utcnow().strftime("%d/%m/%Y")
                self.feed = "\n".join([f"• {i.title}" for i in res.motds])

                print(Fore.GREEN + f"News changed at {self.date}")
                newsgenerator = NewsGenerator(self)
                newsgenerator.main(res.motds)

                if self.tweetNews:
                    self.tweet_news()

            time.sleep(self.delay)
            count += 1
        
    def tweet_news(self):
        name = self.name
        feed = self.feed
        date = self.date

        try:
            self.twitter.update_with_media(
                "Cache/br.gif",
                f"#Fortnite News Update for {date}:\n\n{feed}\n[{name}]"
            )
            print(Fore.GREEN + "Tweeted image!")
        except Exception as e:
            print(Fore.RED + "News Feed [{e}]")