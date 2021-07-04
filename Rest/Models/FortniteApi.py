class NewCosmetics:
    def __init__(self, data):
        self.build = data.get('build', '')
        self.previousBuild = data.get('previousBuild', '')
        self.hash = data.get('hash', '')
        self.date = data.get('date')
        self.lastAddition = data.get('lastAddition')
        self.items = [Cosmetic(i) for i in data.get('items')]


class Cosmetic:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.type = Information(
            data.get('type', {})) if data.get('type') else None
        self.rarity = Information(
            data.get('rarity', {})) if data.get('rarity') else None
        self.series = Information(
            data.get('series', {})) if data.get('series') else None
        self.set = Information(
            data.get('set', {})) if data.get('set') else None
        self.introduction = Introduction(
            data.get('introduction', {})) if data.get('introduction') else None
        self.images = Images(data.get('images', {}))
        self.variants = data.get('variants')
        self.gameplayTags = [i for i in data.get(
            'gameplayTags', [])] if data.get('gameplayTags') else []
        self.dynamicPakId = data.get('dynamicPakId')
        self.added = data.get('added')
        self.shopHistory = data.get('shopHistory', [])


class Information:
    def __init__(self, data):
        self.value = data.get('value')
        self.displayValue = data.get('displayValue')
        self.text = data.get('text')
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
        self.mainKey = data.get('mainKey')
        self.dynamicKeys = [i for i in data.get('dynamicKeys')]
        self.updated = data.get('updated')


class DynamicKey:
    def __init__(self, data):
        self.pakFilename = data.get('pakFilename')
        self.pakGuid = data.get('pakGuid')
        self.key = data.get('key')
