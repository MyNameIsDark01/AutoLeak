from colorama import Fore
from getch import pause

from Utilities.BaseIcon import BaseIcon
from Utilities.ImageUtil import ImageUtil


class CosmeticSearch:
    def __init__(self, data):
        self.log = data.log
        self.platform = data.platform

        self.watermark = data.watermark
        self.placeholder = data.placeholder

        self.api = data.api[0]
        self.language = data.language

    def search(self):
        self.log.info(Fore.GREEN + 'What cosmetic do you want to grab?')
        ask = input()

        cosmetic = self.api.search_cosmetic(cosmetic=ask)
        if not cosmetic:
            exit(pause(Fore.RED + f'Unable to retrieve {ask}.'))

        base = BaseIcon(self)
        image_list = [base.main(i) for i in cosmetic]
        if len(image_list) > 1:
            image = base.merge_icons(image_list, f'{ask}.jpg')
        else:
            image = image_list[0]

        if self.platform == 'Windows':
            image.show()

    def pak(self):
        self.log.info('What number pak do you want to grab?')
        ask = input()

        cosmetic = self.api.search_cosmetic(pak_id=ask)
        if not cosmetic:
            exit(pause(print(Fore.RED + f'Unable to retrieve {ask}.')))

        base = BaseIcon(self)
        image_list = [base.main(i) for i in cosmetic]
        if len(image_list) > 1:
            image = base.merge_icons(image_list, f'{ask}.jpg')
        else:
            image = image_list[0]

        if self.platform == 'Windows':
            image.show()

