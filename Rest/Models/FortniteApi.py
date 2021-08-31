import json


class NewCosmetics:
    def __init__(self, data):
        self.build = data.get('build', '')
        self.previousBuild = data.get('previousBuild', '')
        self.hash = data.get('hash', '')
        self.date = data.get('date')
        self.lastAddition = data.get('lastAddition')
        self.items = [Cosmetic(i) for i in data.get('items')]

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class ShopV2:
    def __init__(self, data):
        self.hash = data.get('hash')
        self.date = data.get('date')
        self.featured = ShopCategory(data.get('featured'))
        self.daily = ShopCategory(data.get('daily'))

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class ShopCategory:
    def __init__(self, data):
        self.name = data.get('name')
        self.entries = [ShopEntry(i) for i in data.get('entries')]


class ShopEntry:
    def __init__(self, data):
        self.regularPrice = data.get('regularPrice')
        self.finalPrice = data.get('finalPrice')
        self.bundle = ShopBundle(data.get('bundle')) if data.get('bundle') else None
        self.banner = Information(data.get('banner')) if data.get('banner') else None
        self.items = [Cosmetic(i) for i in data.get('items')]


class ShopBundle:
    def __init__(self, data):
        self.name = data.get('name')
        self.info = data.get('info')
        self.image = data.get('image')


class Cosmetic:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.type = Information(data.get('type', {})) if data.get('type') else None
        self.rarity = Information(data.get('rarity', {})) if data.get('rarity') else None
        self.series = Information(data.get('series', {})) if data.get('series') else None
        self.set = Information(data.get('set', {})) if data.get('set') else None
        self.introduction = Introduction(data.get('introduction', {})) if data.get('introduction') else None
        self.images = Images(data.get('images', {}))
        self.variants = data.get('variants')
        self.gameplayTags = [i for i in data.get('gameplayTags', [])] if data.get('gameplayTags') else []
        self.dynamicPakId = data.get('dynamicPakId')
        self.added = data.get('added')
        self.shopHistory = data.get('shopHistory', [])


class Information:
    def __init__(self, data):
        self.value = data.get('value')
        if data.get('intensity'):
            self.intensity = data.get('intensity')

        if data.get('displayValue'):
            self.displayValue = data.get('displayValue')

        if data.get('text'):
            self.text = data.get('text')
        
        if data.get('image'):
            self.image = data.get('image')
        self.backendValue = data.get('backendValue')


class Introduction:
    def __init__(self, data):
        self.chapter = data.get('chapter')
        self.season = data.get('season')
        self.text = data.get('text')
        self.backendValue = data.get('backendValue')


class Images:
    def __init__(self, data):
        self.smallIcon = data.get('smallIcon')
        self.icon = data.get('icon')
        self.featured = data.get('featured')
        self.other = data.get('other')


class Build:
    def __init__(self, data):
        self.build = data.get('build')
        self.mainKey = '0x' + data.get('mainKey')
        self.dynamicKeys = [i for i in data.get('dynamicKeys')]
        self.updated = data.get('updated') # Not used yet

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class DynamicKey:
    def __init__(self, data):
        self.pakFilename = data.get('pakFilename')
        self.pakGuid = data.get('pakGuid')
        self.key = '0x' + data.get('key')


class NewsV2:
    def __init__(self, data):
        self.hash = data.get('hash')
        self.date = data.get('date')
        self.image = data.get('image')
        self.motds = [BRNewsV2(i) for i in data.get('motds', [])] if data.get('motds') else []

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class BRNewsV2:
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.tabTitle = data.get('tabTitle')
        self.body = data.get('body')
        self.image = data.get('image')
        self.tileImage = data.get('tileImage')