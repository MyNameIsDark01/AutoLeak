import time
import os
import glob
import json

from colorama import Fore
from getch import pause

from Utilities.BaseIcon import BaseIcon
from Rest.Models.FortniteApi import Build, NewCosmetics


class BuildUpdate:
    def __init__(self, data):
        self.log = data.log

        self.name = data.name
        self.footer = data.footer
        self.language = data.language
        self.watermark = data.watermark
        self.placeholder = data.placeholder
        
        self.twitter = data.twitter
        self.tweetUpdate = data.tweetUpdate
        self.tweetAes = data.tweetAes
        self.tweetCosmetics = data.tweetCosmetics
        self.cosmeticText = data.cosmeticText

        self.api = data.api[0]
        if data.benBot:
            self.api = data.api[2]
        
        self.delay = data.delay

    def main(self):

        count = 1

        while True:
            self.log.info(Fore.YELLOW + f'Checking for changes: -> [{count}]')
            aes = self.api.get_build()
            if not aes:
                time.sleep(self.delay)
                continue

            if not os.path.isfile('Cache/Aes.json'):
                open('Cache/Aes.json', 'w+').write(aes.json())
                count += 1
                time.sleep(self.delay)
                continue

            old_aes = Build(json.loads(open('Cache/aes.json').read()))

            if aes != old_aes:
                open('Cache/Aes.json', 'w+').write(aes.json())

            build = aes.build
            old_build = old_aes.build

            aeskey = aes.mainKey
            old_aeskey = old_aes.mainKey

            if build != old_build:
                self.log.info(Fore.YELLOW + f'Detected build update! -> [{count}]')
                if self.tweetUpdate:
                    self.tweet_build(build)

            if aeskey != old_aeskey:
                self.log.info(Fore.YELLOW + f'Detected Aes update! -> [{count}]')
                if self.tweetAes:
                    self.tweet_aes(aeskey)

                for filename in glob.glob('Cache/images/*.png'):
                    os.remove(filename)

            new_cosmetics = self.api.new_cosmetics()
            if not new_cosmetics:
                time.sleep(self.delay)
                continue

            if not os.path.isfile('Cache/newCosmetics.json'):
                open('Cache/newCosmetics.json', 'w+').write(new_cosmetics.json())
                count += 1
                time.sleep(self.delay)
                continue

            old_cosmetics = NewCosmetics(json.loads(
                open('Cache/newCosmetics.json').read()))

            if old_cosmetics != new_cosmetics:
                open('Cache/newCosmetics.json', 'w+').write(new_cosmetics.json())

            if new_cosmetics.build == aes.build and old_cosmetics.build != new_cosmetics.build and new_cosmetics.hash != old_cosmetics.hash:
                self.log.info(Fore.YELLOW + f'New Cosmetics detected! -> [{count}]')
                self.log.info(Fore.BLUE + '\Generating icons...\n')

                self.create_new_cosmetics()
                if self.tweetCosmetics:
                    self.tweet_cosmetics()

            elif new_cosmetics.hash != old_cosmetics.hash:
                self.log.info(Fore.YELLOW + f'New Cosmetics decrypted! -> [{count-1}]')
                self.log.info(Fore.BLUE + '\Generating icons...\n')

                old = [i.id for i in old_cosmetics.items]
                new = [i for i in new_cosmetics.items if i.id not in old]

                self.create_new_cosmetics(new)
                if self.tweetCosmetics:
                    self.tweet_cosmetics()

            time.sleep(self.delay)
            count += 1

    def create_new_cosmetics(self, new_cosmetics: list = None):
        start_time = time.time()

        if not new_cosmetics:
            new_cosmetics = self.api.new_cosmetics().items

        baseIcon = BaseIcon(self)

        image_list = []

        count = 1
        for i in new_cosmetics:
            image_list.append(baseIcon.main(i))

            percentage = (count/len(new_cosmetics)) * 100
            self.log.info(Fore.CYAN + f"Generated image for {i.id}")
            self.log.info(Fore.CYAN + f"{count}/{len(new_cosmetics)} - {round(percentage)}%\n")
            count += 1

        baseIcon.merge_icons(image_list, 'NewCosmetics.jpg')
        print("!  !  !  !  !  !  !")
        print(f"IMAGE GENERATING COMPLETE - Generated images in {round(time.time() - start_time, 2)} seconds")
        print("!  !  !  !  !  !  !")

    def tweet_build(self, build):
        name = self.name
        footer = self.footer

        try:
            self.twitter.update_status(f"[{name}] Current Fortnite build:\n\n{build}\n\n{footer}")
            self.log.info(Fore.GREEN+ "Tweeted current build!")
        except Exception as e:
            self.log.error(Fore.RED + f"Failed to tweet build! ({e})")

    def tweet_aes(self, key):
        name = self.name
        footer = self.footer

        try:
            self.twitter.update_status(f"[{name}] Current Fortnite AES Key:\n\n{key}\n\n{footer}")
            self.log.info(Fore.GREEN+ "Tweeted current aes key!")
        except Exception as e:
            self.log.error(Fore.RED + f"Failed to tweet aes key! ({e})")

    def tweet_cosmetics(self):
        name = self.name
        text = self.cosmeticText

        try:
            self.twitter.update_with_media(f'Cache/NewCosmetics.jpg', f'[{name}] {text}')
            self.log.info(Fore.GREEN+ "Tweeted new cosmetics!")
        except Exception as e:
            self.log.error(Fore.RED + f"Failed to tweet new cosmetics! ({e})")
