# Wallhaven Auto Downloader

Simple script to automatically download wallpapers from a [Wallhaven](https://wallhaven.cc/) collection.

## How to use
**IMPORTANT: The collection has to be public for the script to work**

Modify the following parameters in the code:
- `collections`: List where every entry is a dictionary of only two keys: `collectionId` and `collectionName`
- `outDir`: Directory where the wallpapers will be downloaded
- `thumbWidth`: Only used for collections with name=browser. Allows for compatibility with my [Browser homepage](https://github.com/ale3d62/browser-homepage). Indicates the width of the resized wallpaper (thumb)

Then just run `python wallhaven_auto_downloader.py`.
