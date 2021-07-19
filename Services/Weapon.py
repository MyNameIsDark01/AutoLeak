from colorama import Fore
from getch import pause

from Utilities.BaseIcon import BaseIcon
from Utilities.ImageUtil import ImageUtil


class Weapon:
    def __init__(self, data):
        self.api = data.api[1]
        self.language = data.language

    def search_weapon(self):
        weapons = None

        method = input('\nDo you want to input an ID (1) or a name (2)? ')
        ask = input(Fore.GREEN + '\nWhat weapon do you want to grab? ')
        if method == '1':
            weapons = self.api.search_weapon(weapon_id=ask)
        elif method == '2':
            weapons = self.api.search_weapon(weapon_name=ask)
        else:
            exit(pause(Fore.RED + "This method doesn't exist."))
            
        if not weapons:
            exit(pause(Fore.RED + "Unable to retrieve data."))

        baseIcon = BaseIcon(self)
        image_list = [baseIcon.main(i) for i in weapons]
        if len(image_list) > 0:
            image = ImageUtil.merge_icons(image_list, f"{ask}.jpg")
        else:
            image = image_list[0]

