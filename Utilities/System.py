import os
import ctypes
import random
import webbrowser

class SystemUtil:
    def __init__(self, data):
        self.platform = data.platform
        self.version = data.version
    
    def create_box(self, platform: str = "Linux"):
        def Mbox(title, text, style):
            return ctypes.windll.user32.MessageBoxW(0, text, title, style)

        if platform != "Windows":
            return 0

        number = random.randint(1, 2)
        if number == 1:
            result = Mbox('AutoLeak - Created by MyNameIsDark01.', f'Hey There! Welcome to AutoLeak, the easiest way to Auto-Leak Fortnite. \nMake sure to join our discord by clicking the OK button!\n\n\nYou are on AutoLeak version v{self.version}!', 0)
            if result == 1:
                webbrowser.open_new('https://discord.gg/UZgHArwp4f')

    def change_title(self):
        plat = self.platform
        self.clear(plat)

        if plat == "Windows":
            os.system("TITLE AutoLeak / Created by MyNameIsDark01.")
        self.create_box(plat)

    def clear(self, platform: str = "Windows"):
        if platform == "Windows":
            os.system("cls")
        elif platform == "Linux":
            os.system("clear")