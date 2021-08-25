import os

from math import ceil
from PIL import Image, ImageDraw, ImageFont
from colorama import Fore

from Utilities.ImageUtil import ImageUtil


class ShopGenerator:
    def __init__(self, data):
        self.language = data.language

        self.primary_font = ImageUtil.get_font(self.language, 'name')
        self.secondary_font = ImageUtil.get_font(self.language, 'description')

    def generateImage(self, item_shop):

        if item_shop.featured:
            featured = item_shop.featured.entries
        else:
            featured = []

        if item_shop.daily:
            daily = item_shop.daily.entries
        else:
            daily = []

        # Determine the max amount of rows for the current Item shop, when
        # there are three columns for both featured and daily, so that we
        # can determine the height of the complete image.

        rows = max(ceil(len(featured) / 5), ceil(len(daily) / 3))
        height = 302 + (300 * rows)

        shop_image = Image.new("RGB", (2544, height))

        background = Image.open(f"Assets/shop/background.png")
        background = ImageUtil.ratio_resize(
            background, shop_image.width, shop_image.height
        )
        shop_image.paste(
            background, ImageUtil.center_x(background.width, shop_image.width, 0)
        )

        logo = Image.open("Assets/shop/logo.png")
        logo = ImageUtil.ratio_resize(logo, 2544, logo.height)
        shop_image.paste(
            logo, ImageUtil.center_x(logo.width, shop_image.width, 0), logo
        )

        canvas = ImageDraw.Draw(shop_image, 'RGB')

        font = ImageFont.truetype(f"Assets/fonts/{self.primary_font}", 48)

        data = "" # date.upper()

        text_width, _ = font.getsize(data)
        canvas.text(
            ImageUtil.center_x(text_width, shop_image.width, 210),
            data,
            (255, 255, 255),
            font=font,
        )

        featured_title = item_shop.featured.name
        daily_title = item_shop.daily.name

        text_width, _ = font.getsize(featured_title)
        canvas.text((1560 / 2 - text_width / 2 - 2, 208), featured_title, (0, 0, 0), font=font)
        canvas.text((1560 / 2 - text_width / 2 + 2, 212), featured_title, (0, 0, 0), font=font)
        canvas.text((1560 / 2 - text_width / 2, 210), featured_title, (255, 255, 255), font=font)

        text_width, _ = font.getsize(daily_title)
        canvas.text(
            (1560 + 964 / 2 - (text_width / 2) - 2, 208),
            daily_title,
            (0, 0, 0),
            font=font,
        )
        canvas.text(
            (1560 + 964 / 2 - (text_width / 2) + 2, 212),
            daily_title,
            (0, 0, 0),
            font=font,
        )
        canvas.text(
            (1560 + 964 / 2 - (text_width / 2), 210),
            daily_title,
            (255, 255, 255),
            font=font,
        )

        bg_fill_shop_section = (0, 0, 0, 64)

        featured_len = len(featured)
        featured_x = 12 + 300*5 if featured_len > 5 else 12+300*featured_len if featured_len > 0 else 0
        featured_y = 12 + 300*ceil(featured_len / 5) if featured_len > 0 else 0

        featured_tile = Image.new('RGBA', (featured_x, featured_y), bg_fill_shop_section)
        # Track which grid position we're at
        i = 0
        for item in featured:
            card: Image = self.generate_card(item)

            if card is not None:
                featured_tile.paste(
                    card,
                    (
                        (12 + ((i % 5) * (card.width + 12))),
                        (12 + ((i // 5) * (card.height + 12))),
                    )
                )

                i += 1
        shop_image.paste(featured_tile, (45, 265), featured_tile)

        daily_len = len(daily)
        daily_x = 12 + 300*3 if daily_len > 3 else 12+300*daily_len if daily_len > 0 else 0
        daily_y = 12 + 300*ceil(daily_len / 3) if daily_len > 0 else 0

        daily_tile = Image.new('RGBA', (daily_x, daily_y), bg_fill_shop_section)
        # Reset grid position
        i = 0
        for item in daily:
            card = self.generate_card(item)

            if card is not None:
                daily_tile.paste(
                    card,
                    (
                        (12 + ((i % 3) * (card.width + 12))),
                        (12 + ((i // 3) * (card.height + 12))),
                    )
                )

                i += 1
        shop_image.paste(daily_tile, (1610, 265), daily_tile)

        try:
            shop_image.save(f"Cache/itemshop.jpg")

            return True
        except Exception as e:
            print(Fore.RED + f"Failed to generate shop [{e}]")


    def generate_card(self, item: dict):
        """Return the card image for the provided Fortnite Item shop item."""

        try:
            name = item.items[0].name
            item_id = item.items[0].id

            icon = item.items[0].images
            if icon.featured:
                icon = icon.featured
            else:
                icon = icon.icon

            is_bundle = False
            bundle_data = item.bundle
            if bundle_data:
                is_bundle = True
                name = bundle_data.name
                icon = bundle_data.image

            regular_price = item.regularPrice
            final_price = item.finalPrice

            series = item.items[0].series
            rarity = item.items[0].rarity
            if rarity:
                rarity = rarity.value
            else:
                rarity = 'Common'

            item_granted = item.items
        except Exception as e:
            print(Fore.RED + f"Failed to parse item, {e}")
            return None

        print(Fore.YELLOW + f"Loading {item_id}...")
        card = Image.new("RGBA", (288, 288))

        try:
            layer = Image.open(f"Assets/BaseIcon/images/card_background_{rarity.lower()}.png")
            layer = ImageUtil.ratio_resize(layer, 288, 288)
        except FileNotFoundError:
            print(rarity)
            print(f"Failed to open card_background_{rarity.lower()}.png")
            layer = Image.open("Assets/BaseIcon/images/card_background_common.png")
            layer = ImageUtil.ratio_resize(layer, 288, 288)

        if layer is not None:
            layer = ImageUtil.ratio_resize(layer, 288, 288)
            card.paste(layer, (0, 0))

        icon = ImageUtil.download_image(icon)
        if icon is not None:
            icon = ImageUtil.ratio_resize(icon, 288, 288)
            card.paste(icon, ImageUtil.center_x(icon.width, card.width, 0), icon)

        if is_bundle is False and len(item_granted) > 1:
            extra = item_granted[1].images
            extra_icon = extra.icon

            extra_icon = ImageUtil.download_image(extra_icon)
            if extra_icon is not None:
                extra_icon = ImageUtil.ratio_resize(extra_icon, 55, 55)

                card.paste(
                    extra_icon,
                    (
                        6,
                        6,
                    ),
                    extra_icon,
                )

        try:
            layer = Image.open(f"Assets/BaseIcon/images/card_faceplate_{rarity.lower()}.png")
            layer = ImageUtil.ratio_resize(layer, 288, 288)
        except FileNotFoundError:
            print(f"Failed to open card_faceplate_{rarity.lower()}.png")
            layer = Image.open("Assets/BaseIcon/images/card_faceplate_common.png")
            layer = ImageUtil.ratio_resize(layer, 288, 288)

        card.paste(layer, (0, 0), layer)

        canvas = ImageDraw.Draw(card)

        vbucks = Image.open("Assets/BaseIcon/vbucks_card.png")
        vbucks = ImageUtil.ratio_resize(vbucks, 17, 17)

        font = ImageFont.truetype(f"Assets/fonts/{self.primary_font}", 17)
        try:
            final_price = str(f"{final_price:,}")
        except ValueError:
            pass
        text_width, text_height = font.getsize(final_price)
        canvas.text(
            (card.width - vbucks.width - text_width - 15, card.height - text_height - 2),
            final_price,
            (255, 255, 255),
            font=font,
        )

        card.paste(
            vbucks,
            (card.width - vbucks.width - 10, card.height - vbucks.height),
            vbucks,
        )
        
        text_size = 32
        font = ImageFont.truetype(f"Assets/fonts/{self.primary_font}", text_size)
        item_name = name.upper()
        text_width, _ = font.getsize(item_name)
        while text_width > 282:
            text_size = text_size - 1
            font = ImageFont.truetype(f"Assets/fonts/{self.primary_font}", text_size)
            text_width, text_height = font.getsize(item_name)

        canvas.text(
            ImageUtil.center_x(text_width, card.width, 240),
            item_name,
            (255, 255, 255),
            font=font,
        )

        return card