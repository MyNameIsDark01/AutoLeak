import hashlib
import json

class NewCosmetics:
    def __init__(self, data):
        self.build = data.get('currentVersion')
        self.previousBuild = data.get('previousVersion')
        self.hash = hashlib.md5(self.build.encode()).hexdigest()
        self.items = [Cosmetic(i) for i in data.get('items')]

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class Cosmetic:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')

        self.type = CosmeticType(data)
        self.rarity = CosmeticRarity(data)
        self.series = CosmeticSeries(data) if data.get('series') else None
        self.set = CosmeticSet(data) if data.get('set') else None
        self.introduction = None
        self.images = Images(data.get('icons', {}))
        self.variants = data.get('variants')
        self.gameplayTags = [i for i in data.get('gameplayTags', [])] if data.get('gameplayTags') else []

class CosmeticType:
    def __init__(self, data):
        self.value = data.get('backendType')
        self.displayValue = data.get('shortDescription')

class CosmeticRarity:
    def __init__(self, data):
        self.backendValue = data.get('backendRarity')
        self.value = self.backendValue.split('::')[1].lower()
        self.displayValue = data.get('rarity')

class CosmeticSeries:
    def __init__(self, data):
        self.backendValue = data.get('backendRarity')
        self.value = data.get('series').get('name')
        self.image = data.get('icons').get('series')

class CosmeticSet:
    def __init__(self, data):
        self.value = data.get('set')
        self.text = data.get('setText')

class Images:
    def __init__(self, data):
        self.smallIcon = None
        self.icon = data.get('icon')
        self.featured = data.get('featured')

class Build:
    def __init__(self, data):
        self.build = data.get('version')
        self.mainKey = data.get('mainKey')
        dKeys = data.get('dynamicKeys')
        self.dynamicKeys = [DynamicKey(i, dKeys[i]) for i in dKeys.keys()]
    
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class DynamicKey:
    def __init__(self, pakFilename, key):
        self.pakFilename = pakFilename
        self.pakGuid = None
        self.key = key