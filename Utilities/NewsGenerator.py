import os
import textwrap
from math import ceil

import requests
from PIL import Image, ImageDraw, ImageFont

from Utilities.ImageUtil import ImageUtil

TitleColor = (255, 255, 255)
DescriptionColor = (51, 236, 254)


class NewsGenerator:
    def __init__(self, data):
        self.language = data.language

        self.primary_font = ImageUtil.get_font(self.language, 'name')
        self.secondary_font = ImageUtil.get_font(self.language, 'description')

    def main(self, news_data: dict):
        image_array: list = [self.generate_image(i, news_data) for i in news_data]
        image_array[0].save(
            'Cache/br.gif',
            save_all=True,
            append_images=image_array[1:],
            duration=5000
        )

    def generate_image(self, data, full_data):
        if data.tabTitle:
            tab_title = data.tabTitle
        else:
            tab_title = data.title

        title = data.title.upper()
        if data.body:
            body = data.body
        else:
            body = ""
        if data.image:
            image = data.image
        else:
            image = 'https://i.imgur.com/Zk0NcmO.jpeg'

        background = Image.new("RGBA", (1280, 720))
        draw = ImageDraw.Draw(background)

        # Image
        news_image = ImageUtil.download_image(image)
        if not news_image:
            return background

        if news_image.width != 1280 or news_image.height != 720:
            news_image = news_image.resize((1280, 720), Image.ANTIALIAS)
        background.paste(news_image, (0, 0))

        # Blu
        blu = Image.open('Assets/news/assets/background.png')
        background.paste(blu, (0, 0), blu)

        # Title
        title_font_size = 50
        title_font = ImageFont.truetype(f'Assets/news/fonts/{self.primary_font}', title_font_size)
        draw.text((25, 520), title, TitleColor, font=title_font)

        # Description
        news_desc = ""
        for desc in body.split("\n"):
            for des in textwrap.wrap(desc, width=56):
                news_desc += f'\n{des}'
        description = news_desc  # Split the Description
        description_font = ImageFont.truetype(f'Assets/News/fonts/{self.secondary_font}', 18)
        draw.multiline_text((25, 560), description,
                            DescriptionColor, font=description_font, spacing=6)

        if tab_title is not None:
            top_title = self.header(full_data, tab_title)
            background.paste(top_title, (0, 0), top_title)

        return background

    def header(self, full_data, n):
        top_ui = Image.new("RGBA", (1280, 75))

        titles = []

        for i in full_data:
            if i.tabTitle:
                titles.append(i.tabTitle)
            elif i.title:
                titles.append(i.title)

        for i, title in enumerate(titles):
            title = title.upper()
            l_titles = len(titles)
            x = (1280 / l_titles)
            card = Image.new('RGBA', (ceil(x), 37))
            canvas = ImageDraw.Draw(card)

            if title == n.upper():
                tint_color = (256, 256, 256)
            else:
                tint_color = (0, 0, 205)

            trasparency = 0.7  # Degree of transparency, 0-100%
            opacity = int(255 * trasparency)

            card_bottom = Image.new("RGBA", (round(x), 37), tint_color)
            draw = ImageDraw.Draw(card_bottom)
            draw.rectangle(((x, 37), (0, 0)), fill=tint_color + (opacity,))

            card.paste(card_bottom, (0, 0), card_bottom)

            font_size = 20
            font = ImageFont.truetype(f'Assets/news/fonts/{self.secondary_font}', font_size)

            text_width, text_height = font.getsize(title)
            while text_width > x - 20:
                font_size = font_size - 1
                font = ImageFont.truetype(f'Assets/news/fonts/{self.secondary_font}', font_size)
                text_width, text_height = font.getsize(title)

            canvas.text(
                ImageUtil.center_x(text_width, card.width, (card.height - text_height)/2),
                title,
                (255, 255, 255),
                font=font,
            )

            top_ui.paste(
                card,
                ((0 + ((i % l_titles) * card.width),
                  (0 + ((i // l_titles) * card.height))))
            )

        return top_ui