from os import path, remove, makedirs
from pathlib import Path

root = Path(".").absolute()

def check_environment():
    "Makes sure some important directories and files exist"

    if not path.exists(root / "storage" / "game"):
        makedirs(root / "storage" / "game")
        print("Created ./storage/game")

    
    print("Environment Initialized")