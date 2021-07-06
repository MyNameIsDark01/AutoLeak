class Weapon:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.rarity = InformationV1(data.get('rarity'))
        self.gameplayTags = [i for i in data.get('gameplayTags', [])] if data.get('gameplayTags') else []
        self.images = ImageV1(data.get('images')) if data.get('images') else None
        self.introduction = None


class InformationV1:
    def __init__(self, data):
        self.value = data


class ImageV1:
    def __init__(self, data):
        self.featured = None
        self.icon = data.get('icon')
        self.smallIcon = None
        self.background = data.get('background')
