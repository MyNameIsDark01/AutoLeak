import time
import os
import glob
from PIL.Image import new

from colorama import Fore
from getch import pause

from Utilities.BaseIcon import BaseIcon
from Utilities.ImageUtil import ImageUtil


class BuildUpdate:
    def __init__(self, data):

        self.name = data.name
        self.footer = data.footer

        self.twitter = data.twitter
        self.tweetUpdate = data.tweetUpdate
        self.tweetAes = data.tweetAes
        self.tweetCosmetics = data.tweetCosmetics
        self.cosmeticText = data.cosmeticText

        self.api = data.api[0]
        self.delay = data.delay
        self.aes = self.api.get_build()
        self.cosmetics = self.api.new_cosmetics()

    def main(self):

        count = 1

        while True:
            print(Fore.YELLOW + f'Checking for changes: -> [{count}]')
            aes = self.api.get_build()
            if not aes:
                time.sleep(self.delay)
                continue

            old_aes = self.aes
            if aes != old_aes:
                self.aes = aes

            build = aes.build
            old_build = old_aes.build

            aeskey = aes.mainKey
            old_aeskey = old_aes.mainKey

            if build != old_build:
                print(Fore.YELLOW + f'\nDetected build update! -> [{count}]')
                if self.tweetUpdate:
                    self.tweet_build()

            if aeskey != old_aeskey:
                print(Fore.YELLOW + f'Detected Aes update! -> [{count}]')
                if self.tweetAes:
                    self.tweet_aes()

                for filename in glob.glob('Cache/images/*.png'):
                    os.remove(filename)

            new_cosmetics = self.api.new_cosmetics()
            if not new_cosmetics:
                continue

            old_cosmetics = self.cosmetics

            if new_cosmetics.build == aes.build and old_cosmetics.build != new_cosmetics.build and \
                    new_cosmetics.hash != old_cosmetics.hash:
                print(Fore.YELLOW + f'New Cosmetics detected! -> [{count}]')
                print(Fore.BLUE + '\nCreating icons...\n')

                self.create_new_cosmetics()
                if self.tweetCosmetics:
                    self.tweet_cosmetics()

                print(
                    Fore.GREEN + "\n!!!!!!!!!!!!!!!!!\nAUTOLEAK COMPLETE\n!!!!!!!!!!!!!!!!!\n")
                exit(pause('Press Any Key To Exit.'))

            elif new_cosmetics.hash != old_cosmetics.hash:
                print(Fore.YELLOW + f'New Cosmetics decrypted! -> [{count-1}]')
                old = [i.id for i in old_cosmetics.items]
                new = [i for i in new_cosmetics.items if i.id not in old]

                self.create_new_cosmetics(new)
                if self.tweetCosmetics:
                    self.tweet_cosmetics()

                print(
                    Fore.GREEN + "\n!!!!!!!!!!!!!!!!!\nAUTOLEAK COMPLETE\n!!!!!!!!!!!!!!!!!\n"
                )
                exit(pause('Press Any Key To Exit.'))

            time.sleep(self.delay)
            count += 1

    def create_new_cosmetics(self, new_cosmetics: list = None):
        if not new_cosmetics:
            new_cosmetics = self.cosmetics.items

        image_list = [
            BaseIcon.main(i, f"{i.id}.png") for i in new_cosmetics
        ]
        ImageUtil.merge_icons(image_list, 'NewCosmetics.jpg')

    def tweet_build(self):
        build = self.aes.build
        name = self.name
        footer = self.footer

        try:
            self.twitter.update_status(
                f"[{name}] Current Fortnite build:\n\n{build}\n\n{footer}"
            )
        except Exception as e:
            print(Fore.RED + f"Failed to tweet build! ({e})")

    def tweet_aes(self):
        key = self.aes.build
        name = self.name
        footer = self.footer

        try:
            self.twitter.update_status(
                f"[{name}] Current Fortnite AES Key:\n\n0x{key}\n\n{footer}"
            )
            print(Fore.GREEN+"Tweeted current aes key!")
        except Exception as e:
            print(Fore.RED + f"Failed to tweet aes key! ({e})")

    def tweet_cosmetics(self):
        name = self.name
        text = self.cosmeticText

        try:
            self.twitter.update_with_media(
                f'Cache/NewCosmetics.jpg', f'[{name}] {text}'
            )
        except Exception as e:
            print(Fore.RED + f"Failed to tweet new cosmetics! ({e})")
