import os

from colorama import Fore
from getch import pause

from Utilities.BaseBundle import generate_bundle

class BundleService:
    def __init__(self, data) -> None:
        from Rest.Getters.FortniteIO import FortniteIO

        self.log = data.log
        self.platform = data.platform

        self.api: FortniteIO = data.api[1]
        self.language = data.language

    def get_challenge_bundles(self):

        challenge_list = self.api.get_challenges()
        if not challenge_list: return exit(pause(Fore.RED + "Unable to retrieve data."))
        #if not os.path.isfile('Cache/challenges.json'):
        #    challenge_list = self.api.get_challenges()
        for idx, i in enumerate(challenge_list):
            print(f"[{idx+1}] {i.get('name')}")

        challenge_bundle_ask = input(Fore.GREEN + '\nSelect the ID relative to challenge to be generated\n')
            
        try:
            challenge_bundle = challenge_list[int(challenge_bundle_ask)-1]
        except KeyError:
            self.log.error(f'{challenge_bundle_ask} is not a valid ID')

        image = generate_bundle(challenge_bundle)
        if self.platform == 'Windows':
            image.show()