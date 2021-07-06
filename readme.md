# AutoLeak

AutoLeak is a terminal-based utility to generate all of the latest leaks in Fortnite, with some bonus features as well.

Make sure to check out our Wiki (to do), with info on how to utilitize [**settings.json**](www.google.com)

# Features

AutoLeak is a program with many features.
Currently, the program features these options:

- Update mode to detect for a new update and leak the contents, saving every one into the image format
- Automatically Tweet Build, AES and New Cosmetics if on update mode
- Generate new cosmetics, which can generate all new cosmetics in an update
- Grab cosmetics from a specific pak (Merging images automatically saves to the new "merged" folder!)
- Search for a cosmetic and generate an image
- Search for a weapon and generate an image
- Merge images by using the new 'Merge Images' command in AutoLeak
- Automatically Tweet out news feed and detect for a change

**Sample Image:**

<p align="left">
    <img src="https://i.imgur.com/OWZQdnF.png" width="512" draggable="false">
</p>

# Requirements

To run AutoLeak, you must have [Python >=3.8](https://www.python.org/downloads/) installed on your computer.

If you want install all requirements in one click open **(install.bat)** or **(install.sh)**

A Fortnite-API API Key isn't required, A FortniteAPI IO Key is required to generate weapons.

# Usage

Open `configuration.py` in your preferred text editor, fill the configurable values. Once finished, save the file.

- `NAME`: The name AutoLeak will use to tweet out something
- `FOOTER`: The name at the bottom of the tweet
- `LANGUAGE`: Set the language for Fortnite Data ([Supported Languages](https://fortnite-api.com/documentation))
- `PLACEHOLDER IMAGE`: Placeholder image to use when item is a placeholder
- `WATERMARK`: Watermark added on image merge (not required)
- `DELAY`: Delay used to check update mode
- `TWITTER`: Your twitter data, to post on twitter, if feed are enabled and tweet text
- `APIKEY`: Your api key to get fortnite data

## Credits

- Fortnite Data provided by [Fortnite-API](https://fortnite-api.com/) and [FortniteIO](https://fortniteapi.io/)
- Cataba assets property of [FModel](https://github.com/iAmAsval/FModel)
- Burbank font property of [Adobe](https://fonts.adobe.com/fonts/burbank)
- Luckiest Guy font property of [Google](https://fonts.google.com/specimen/Luckiest+Guy)
