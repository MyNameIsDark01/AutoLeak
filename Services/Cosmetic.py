from colorama import Fore
from getch import pause

from Utilities.BaseIcon import BaseIcon
from Utilities.ImageUtil import ImageUtil


class CosmeticSearch:
    def __init__(self, data):
        self.api = data.api[0]
        self.language = data.language

    def search(self):
        print(Fore.GREEN + '\nWhat cosmetic do you want to grab?')
        ask = input()

        cosmetic = self.api.search_cosmetic(cosmetic=ask)
        if not cosmetic:
            exit(pause(Fore.RED + f'Unable to retrieve {ask}.'))

        base = BaseIcon(self)
        image_list = [base.main(i) for i in cosmetic]
        if len(image_list) > 1:
            image = ImageUtil.merge_icons(image_list, f'{ask}.jpg')
        else:
            image = image_list[0]

        image.show()

    def pak(self):
        print('\nWhat number pak do you want to grab?')
        ask = input()

        cosmetic = self.api.search_cosmetic(pak_id=ask)
        if not cosmetic:
            exit(pause(print(Fore.RED + f'Unable to retrieve {ask}.')))

        base = BaseIcon(self)
        image_list = [base.main(i) for i in cosmetic]
        if len(image_list) > 1:
            image = ImageUtil.merge_icons(image_list, f'{ask}.jpg')
        else:
            image = image_list[0]

        image.show()
