import json
import colorama

from getch import pause
from colorama import Fore
from typing import Union, List

from Rest.Getters.FortniteApi import FortniteApi
from Rest.Getters.FortniteIO import FortniteIO

from Services.NewUpdate import BuildUpdate
from Services.Weapon import Weapon
from Services.Cosmetic import CosmeticSearch
from Services.News import News
from Services.Shop import ShopUpdate
from Services.Section import ShopSection


from Utilities.Errors import NoDigit
from Utilities.Twitter import TwitterClient
from Utilities.ImageUtil import ImageUtil
from Utilities.System import SystemUtil


colorama.init(autoreset=True)


class Main:
    def __init__(self):
        try:
            self.version = 1.4
            
            settings = json.loads(open("settings.json").read())

            self.name = settings.get('name')
            self.footer = settings.get('footer')

            language = settings.get('language')
            check = self.check_language_code(language)
            self.language = language if check else 'en'

            twitter = settings.get('twitter', {})
            self.twitter = None
            self.tweetUpdate = twitter.get('tweetUpdate', False)
            self.tweetAes = twitter.get('tweetAes', False)
            self.tweetCosmetics = twitter.get('tweetCosmetics', False)
            self.tweetNews = True
            self.tweetShop = True
            self.tweetSection = True

            self.cosmeticText = twitter.get('cosmeticText', '')
            self.shopText = twitter.get('shopText', '')
            self.shopSectionText = twitter.get('shopSectionText', '')
            
            if twitter.get('isEnabled'):
                apiKey = twitter.get('apiKey')
                apiSecret = twitter.get('apiSecret')
                accessToken = twitter.get('accessToken')
                accessTokenSecret = twitter.get('accessTokenSecret')
                self.twitter = TwitterClient(
                    apiKey, apiSecret, accessToken, accessTokenSecret
                )
            else:
                self.tweetUpdate = False
                self.tweetAes = False
                self.tweetCosmetics = False
                self.tweetNews = False
                self.tweetShop = False
                self.tweetSection = False

            self.key = [
                settings.get('apiKey', {})[i]
                for i in list(settings.get('apiKey', {}))
            ]
            self.api = [FortniteApi(self), FortniteIO(self)]
            self.delay = settings.get('delay', 5)
        except json.decoder.JSONDecodeError:
            exit(pause(Fore.RED + 'Wrong json formatting.'))
        except FileNotFoundError:
            exit(pause(Fore.RED + "Settings.json not found."))
        except Exception as e:
            exit(pause(Fore.RED + f'An error occurred {e}.'))

    # ==> Main Thread
    def main(self):
        SystemUtil(self).change_title()
        self.welcome()
        choice = input('>> ')
        try:
            check_choice = self.get_choices(choice)
        except NoDigit:
            print('No Digit')
            return 0

        if check_choice:
            check_choice()
        else:
            print("Command not available")

    def welcome(self) -> None:
        print("""
    ░█████╗░██╗░░░██╗████████╗░█████╗░██╗░░░░░███████╗░█████╗░██╗░░██╗
    ██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██║░░░░░██╔════╝██╔══██╗██║░██╔╝
    ███████║██║░░░██║░░░██║░░░██║░░██║██║░░░░░█████╗░░███████║█████═╝░
    ██╔══██║██║░░░██║░░░██║░░░██║░░██║██║░░░░░██╔══╝░░██╔══██║██╔═██╗░
    ██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝███████╗███████╗██║░░██║██║░╚██╗
    ╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝""")

        print(Fore.GREEN + "\n- - - - - MENU - - - - -")
        print("")
        print(Fore.RED+'!!NOTICE!! ' + Fore.GREEN + 'We have just introduced new icons into AutoLeak!')
        print(Fore.YELLOW + "(1)" + Fore.GREEN + " - Start update mode")
        print(Fore.YELLOW + "(2)" + Fore.GREEN + " - Generate new cosmetics")
        print("(3) - Grab all cosmetics from a specific pak")
        print("(4) - Search for a cosmetic")
        print("(5) - Search for any weapon of choice.")
        print("(6) - Merge images in icons folder")
        print("(7) - Check for a change in News Feed")
        print("(8) - Check for a change in Shop Sections")
        print("(9) - Check for a change in Item Shop")

    def check_twitter_auth(self):
        if self.twitter.verify_credentials() is False:
            print(Fore.RED + 'Twitter Invalid Credentials\nTweetUpdate, TweetAes and TweetCosmetics loaded as False')

            self.tweetUpdate = False
            self.tweetAes = False
            self.tweetCosmetics = False

    def check_language_code(self, lang: str) -> bool:
        languages: List[str] = [
            'ar', 'de', 'en', 'es', 'es-419', 'fr', 'it', 'ja', 'ko', 'pl', 'pt-BR', 'ru', 'tr', 'zh-CN', 'zh-Hant'
        ]

        return True if lang in languages else False

    def get_choices(self, x: Union[str, int, None]):
        build = BuildUpdate(self)
        cosmetic = CosmeticSearch(self)
        weapon = Weapon(self)
        imageUtil = ImageUtil()
        news = News(self)
        shopgen = ShopUpdate(self)
        shopsection = ShopSection(self)

        choices = {
            1: build.main,
            2: build.create_new_cosmetics,
            3: cosmetic.pak,
            4: cosmetic.search,
            5: weapon.search_weapon,
            6: imageUtil.merge_icons,
            7: news.main,
            8: shopsection.main,
            9: shopgen.main
        }

        if isinstance(x, str):
            if x.isdigit():
                x = int(x)
            else:
                raise NoDigit

        return choices.get(x, None)


if __name__ == '__main__':
    try:
        Main().main()
    except KeyboardInterrupt:
        exit()
