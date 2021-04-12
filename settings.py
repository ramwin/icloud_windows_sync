import pathlib


DEFAULT_BACK_PATH = pathlib.Path("D:/AVA/iphone相册/icloud/")
CLOUD_PATH = pathlib.Path.home().joinpath("Pictures/iCloud Photos/Photos")
BACK_PATH = input(f"input your backup directory path: {DEFAULT_BACK_PATH}") or DEFAULT_BACK_PATH
