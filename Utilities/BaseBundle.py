import requests

from typing import Union
from PIL import Image, ImageDraw, ImageFont

from Utilities.ImageUtil import ImageUtil

class TandemCharacter:
    def __init__(self, data):
        self.id = data.get('id')
        self.displayName = data.get('displayName')
        self.images = TandemImages(data.get('images'))

class TandemImages:
    def __init__(self, data):
        self.toast = data.get('toast')
        self.sidePanel = data.get('sidePanel')
        self.entryList = data.get('entryList')


class QuestXP:
    def __init__(self, xp):
        self.icon = 'https://i.imgur.com/idyLjvo.png'
        self.text = f'x{xp}'

class QuestItem:
    def __init__(self, data):
        images = data.get('images')
        if images.get('featured'):
            self.icon = images.get('featured')
        elif images.get('icon'):
            self.icon = images.get('icon')
        self.text = data.get('name', '')

class BaseBundle:
    def __init__(self, data):
        self.width = 1024
        self.headerHeight = 40
        self.additionalSize = 0

        self.id = data.get('id')
        self.displayName = data.get('name')
        self.tags = data.get('tags')

        self.images = data.get('images')
        
        #self.completitionQuest = [CompletionReward(i) for i in data.get('bundleRewards')]
        self.quests = [Quest(i) for i in data.get('quests')] + [CompletionReward(i) for i in data.get('bundleRewards')]
        self.additionalSize += 256 * len(self.quests)

    @staticmethod
    def drawHeader(canvas: ImageDraw.Draw, icon):
        canvas.rectangle(
            [(0, 0), (icon.width, icon.headerHeight)],
            fill=(113,0,4),
        )
    
    @staticmethod
    def drawDisplayName(canvas: ImageDraw, icon):
        if not icon.displayName: return

        text_size = 24
        font = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', text_size)
        
        text = icon.displayName.upper()

        text_width, text_height = font.getsize(text)
        x = (icon.width - text_width) / 2
        y = (icon.headerHeight - text_height) / 2
        while text_width > (icon.width - 100):
            text_size = text_size - 1
            font = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', text_size)
            text_width, _ = font.getsize(text)
            x = (icon.width - text_width) / 2
            y = (icon.headerHeight - text_height) / 2
        
        canvas.text(
            (x, y),
            text,
            fill=(255, 255, 255),
            font=font,
            align='left'
        )

    @staticmethod
    def drawQuests(ret, canvas: ImageDraw, icon):
        y = icon.headerHeight
        for quest in icon.quests:
            quest.drawQuest(ret, canvas, y)
            y += quest.height

class Quest:
    def __init__(self, data):
        if data is None:
            return

        self.margin = 0
        self.width = 1024
        self.height = 256

        self.displayName = data.get('name')
        self.count = data.get('progressTotal')
        self.tandem = TandemCharacter(data.get('tandemCharacter', {})) if data.get('tandemCharacter') else None
        self.reward = QuestReward(data.get('reward'))

        self.titleFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', 40)
        self.descriptionFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', 16)
        self.rewardFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', 25)

    def drawQuest(self, ret, canvas: ImageDraw, y: int):
        self.drawBackground(canvas, y)
        self.drawPreview(ret, y)
        self.drawTexts(ret, canvas, y)

    def drawBackground(self, canvas: ImageDraw, y: int):
        canvas.rectangle(
            [(self.margin, y), (self.width, y + self.height)],
            fill=(150, 0, 0),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.width, y + self.height)],
            fill=(113,0,4),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.width, y + self.height)],
            fill=(113,0,4),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.height / 2 + 100, y + self.height)],
            fill=(113,0,4),
        )

    
    def drawPreview(self, ret, y: int):
        if not self.tandem or not self.tandem.images.sidePanel: return
        
        image = ImageUtil.download_image(self.tandem.images.sidePanel)
        image = ImageUtil.ratio_resize(image, 256, 256)
        ret.paste(image, (self.margin, y), image)

    def drawTexts(self, ret, canvas: ImageDraw, y: int):
        if self.displayName and len(self.displayName.strip()) > 0:
            text_width, text_height = self.titleFont.getsize(self.displayName)
            while text_width > (self.width - self.height - 100):
                self.titleFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', self.titleFont.size - 1)
                text_width, _ = self.titleFont.getsize(self.displayName)
            canvas.text(
                (self.height, y + 50),
                text=self.displayName,
                font=self.titleFont,
                fill='white'
            )

            outY = y + 105            
            canvas.rectangle(
                [(self.height, outY), (self.width - 150, outY + 5)],
                fill=(200, 0, 0),
            )

            if self.count > 0:
                canvas.text(
                    (self.width - 130, outY - 10),
                    text=f'0 / {self.count}',
                    font=self.rewardFont,
                    fill='white',
                    stroke_width=1,
                    stroke_fill=(0,0,0)
                )
            
            self.reward.drawReward(ret, canvas, outY, y)

class CompletionReward:
    def __init__(self, data):
        if data is None:
            return

        self.margin = 0
        self.width = 1024
        self.height = 256

        self.displayName = 'Complete ALL CHALLENGES to earn the reward item'
        self.count = 0

        reward = {'items': [data]}
        self.reward = QuestReward(reward)

        self.titleFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', 40)
        #self.descriptionFont = ImageFont.truetype('BurbankBigCondensed-Black.otf', 16)
        #self.rewardFont = ImageFont.truetype('BurbankBigCondensed-Black.otf', 25)
    
    def drawQuest(self, ret, canvas: ImageDraw, y: int):
        self.drawBackground(canvas, y)
        self.drawTexts(ret, canvas, y)

    def drawBackground(self, canvas: ImageDraw, y: int):
        canvas.rectangle(
            [(self.margin, y), (self.width, y + self.height)],
            fill=(150, 0, 0),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.width, y + self.height)],
            fill=(113,0,4),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.width, y + self.height)],
            fill=(113,0,4),
        )

        canvas.rectangle(
            [(self.height / 2, y), (self.height / 2 + 100, y + self.height)],
            fill=(113,0,4),
        )

    def drawTexts(self, ret, canvas: ImageDraw, y: int):
        if self.displayName and len(self.displayName.strip()) > 0:
            text_width, text_height = self.titleFont.getsize(self.displayName)
            while text_width > (self.width - self.height - 100):
                self.titleFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', self.titleFont.size - 1)
                text_width, _ = self.titleFont.getsize(self.displayName)
            canvas.text(
                (self.height, y + 50),
                text=self.displayName,
                font=self.titleFont,
                fill='white'
            )

            outY = y + 105            
            canvas.rectangle(
                [(self.height, outY), (self.width - 150, outY + 5)],
                fill=(200, 0, 0),
            )

            if self.count > 0:
                canvas.text(
                    (self.width - 130, outY - 10),
                    text=f'0 / {self.count}',
                    font=self.rewardFont,
                    fill='white',
                    stroke_width=1,
                    stroke_fill=(0,0,0)
                )
            
            self.reward.drawReward(ret, canvas, outY, y)

class QuestReward:
    def __init__(self, data):
        if data is None:
            return

        self.reward: Union[QuestItem, QuestXP, None] = None
        if data.get('xp', 0) > 0:
            self.reward = QuestXP(data.get('xp'))
        elif len(data.get('items', [])) > 0:
            self.reward = QuestItem(data.get('items')[0])

        self.textFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', 50)
    
    def drawReward(self, ret, canvas, outY: int, y: int):
        #canvas.rectangle([(256, outY+25), (1024-20, y + 256 - 25)])

        if self.reward:
            image_width = 101
            if self.reward.icon:
                image = ImageUtil.download_image(self.reward.icon)
                image = ImageUtil.ratio_resize(image, 101, 101)
                image_width = image.width
                ret.paste(image, (256, outY+25), image)

            text_width, text_height = self.textFont.getsize(self.reward.text)
            while text_width > 748:
                self.textFont = ImageFont.truetype('Assets/fonts/BurbankBigCondensed-Black.otf', self.textFont.size - 1)
                text_width, _ = self.textFont.getsize(self.reward.text)
            
            canvas.text(
                (256 + image_width + 25, outY + 70 - 20),
                text=self.reward.text,
                font=self.textFont,
                fill=(230,253,177),
                stroke_width=1,
                stroke_fill=(129, 141, 96)
            )

        else:
            canvas.text(
                (256, y + 170 - 20),
                text="No Reward",
                fill='white',
                font=self.textFont
            )

def generate_bundle(bundle: dict):
    icon: BaseBundle = BaseBundle(bundle)
    print("Generating " + icon.displayName + "...")
    ret = Image.new(
        'RGBA',
        (icon.width, icon.headerHeight + icon.additionalSize),
        )
    canvas = ImageDraw.Draw(ret)
    BaseBundle.drawHeader(canvas, icon)
    BaseBundle.drawDisplayName(canvas, icon)
    BaseBundle.drawQuests(ret, canvas, icon)

    ret.save(f'Cache/bundles/{icon.id}.png')
    return ret