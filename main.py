import json
import colorama

from getch import pause
from colorama import Fore
from typing import Union, List

from Rest.Getters.FortniteApi import FortniteApi
from Rest.Getters.FortniteIO import FortniteIO

from Services.NewUpdate import BuildUpdate

from Utilities.Errors import NoDigit
from Utilities.Twitter import TwitterClient

colorama.init(autoreset=True)


class Main:
    def __init__(self):
        try:
            settings = json.loads(open("settings.json").read())

            self.name = settings.get('name')
            self.footer = settings.get('footer')

            language = settings.get('language', 'en')
            check = self.check_language_code(language)
            self.language = language if check else 'en'

            twitter = settings.get('twitter', {})
            self.twitter = None
            if twitter.get('isEnabled'):
                apiKey = twitter.get('apiKey')
                apiSecret = twitter.get('apiSecret')
                accessToken = twitter.get('accessToken')
                accessTokenSecret = twitter.get('accessTokenSecret')
                self.twitter = TwitterClient(
                    apiKey, apiSecret, accessToken, accessTokenSecret
                )
                self.tweetUpdate = twitter.get('tweetUpdate', False)
                self.tweetAes = twitter.get('tweetAes', False)
                self.tweetCosmetics = twitter.get('tweetCosmetics', False)
                self.cosmeticText = twitter.get('cosmeticText', '')

            self.key = [
                settings.get('apiKey', {})[i]
                for i in list(settings.get('apiKey', {}))
            ]
            self.api = [FortniteApi(self), FortniteIO(self)]
            self.delay = settings.get('delay', 5)
        except json.decoder.JSONDecodeError:
            exit(pause(Fore.RED + 'Wrong json formatting'))
        except Exception as e:
            exit(pause(Fore.RED + 'An error occurred %s' % e))

    # ==> Main Thread
    def main(self):
        self.welcome()
        choice = input('>>')
        try:
            check_choice = self.get_choices(choice)
        except NoDigit:
            print('No Digit')
            return 0

        if check_choice:
            print('Starting...')
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
        print(Fore.RED+'!!NOTICE!! '+Fore.GREEN +
              'We have just introduced new icons into AutoLeak! These are in beta, but you\ncan test them out by changing the iconType in settings.json to "new"!\n')
        print(Fore.YELLOW + "(1)" + Fore.GREEN + " - Start update mode")
        print(Fore.YELLOW + "(2)" + Fore.GREEN + " - Generate new cosmetics")
        print("(3) - Tweet current build")
        print("(4) - Tweet current AES key")
        print("(5) - Search for a cosmetic")
        print("(6) - Clear contents of the icon folder")
        print("(7) - Check for a change in News Feed")
        print("(8) - Merge images in icons folder")
        print("(9) - Check for a change in Shop Sections")
        print("(10) - Check for a change in Item Shop")
        print("(11) - Grab all cosmetics from a specific pak")
        print("(12) - Checks for a change in notices")
        print("(13) - Checks for a change in staging servers")
        print("(14) - Search for any weapon of choice.")

    def check_twitter_auth(self):
        if self.twitter.verify_credentials() is False:
            print(
                Fore.RED + 'Twitter Invalid Credentials\nTweetUpdate, TweetAes and TweetCosmetics loaded as False'
            )

            self.tweetUpdate = False
            self.tweetAes = False
            self.tweetCosmetics = False

    def check_language_code(self, lang: str) -> bool:
        languages: List[str] = [
            'ar', 'de', 'en', 'es', 'es-419', 'fr', 'it', 'ja', 'ko', 'pl', 'pt-BR', 'ru', 'tr', 'zh-CN', 'zh-Hant'
        ]

        return True if lang in languages else False

    def get_choices(self, x: Union[str, int]):
        choices = {
            1: BuildUpdate(self).main,
            2: BuildUpdate(self).create_new_cosmetics,
            3: BuildUpdate(self).tweet_build,
            4: BuildUpdate(self).tweet_aes
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
