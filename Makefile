# NOTE: these commands expect the environment to be set up a certain way. Maybe later I'll make this reproducible...

.RECIPEPREFIX = >
.PHONY: linux windows all

linux:
> ~/.venv/base/bin/pyinstaller --name steam-recommendation-scraper_LINUX --clean --onefile gui.py scraper.py

windows:
> wine "C:\Program Files\Python310\Scripts\pyinstaller.exe" --name steam-recommendation-scraper_WIN --workpath ~/Documents/build --clean --onefile --windowed gui.py scraper.py

all: linux windows

