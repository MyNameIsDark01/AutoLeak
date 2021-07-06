import requests
import glob

from math import sqrt, ceil
from PIL import Image
from typing import List, Union


class ImageUtil:
    @staticmethod
    def open():
        return

    @staticmethod
    def get_font(language: str, text_type: str) -> Union[str, None]:
        font_list = {
            "name": {
                "default": "BurbankBigRegular-BlackItalic.otf",
                "ko": "AsiaERINM.otf",
                "ru": "BurbankBigCondensed-Black.otf",
                "ja": "NIS_JYAU.otf",
                "ar": "NotoSansArabic-Black.otf",
                "zh-CN": "NotoSansSC-Black.otf",
                "zh-Hant": "NotoSansSC-Black.otf"
            },
            "description": {
                "default": "BurbankSmall-BlackItalic.otf",
                "ko": "NotoSansKR-Regular.otf",
                "ja": "NotoSansJP-Bold.otf",
                "ar": "NotoSansArabic-Regular.otf",
                "zh-CN": "NotoSansSC-Regular.otf",
                "zh-Hant": "NotoSansSC-Regular.otf"
            }
        }
        font_type = font_list.get(text_type)
        return font_type.get(language, font_type.get('default'))

    @staticmethod
    def download_image(url):
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            return Image.open(res.raw).convert('RGBA')
    
    @staticmethod
    def center_x(foreground_width: int, background_width: int):
        """Return the tuple necessary for horizontal centering and an optional vertical distance."""

        return int(background_width / 2) - int(foreground_width / 2)

    @staticmethod
    def ratio_resize(image: Image.Image, max_width: int, max_height: int):
        """Resize and return the provided image while maintaining aspect ratio."""

        ratio = max(max_width / image.width, max_height / image.height)

        return image.resize(
            (int(image.width * ratio), int(image.height * ratio)), Image.ANTIALIAS
        )

    @staticmethod
    def merge_icons(datas: Union[list, None] = None, save_as: str = 'merge.jpg'):
        if not datas:
            datas = [Image.open(i) for i in glob.glob('Cache/images/*.png')]

        print('\nMerging images...')
        row_n = len(datas)
        rowslen = ceil(sqrt(row_n))
        columnslen = round(sqrt(row_n))

        mode = "RGB"
        px = 512

        rows = rowslen * px
        columns = columnslen * px
        image = Image.new(mode, (rows, columns))

        i = 0

        for card in datas:
            image.paste(
                card,
                ((0 + ((i % rowslen) * card.width)),
                 (0 + ((i // rowslen) * card.height)))
            )

            i += 1

        if save_as and len(save_as) > 4:
            image.save(f"Cache/{save_as}")

        return image
