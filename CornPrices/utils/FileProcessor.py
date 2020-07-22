import pickle
from os import path, remove, makedirs
from pathlib import Path
from CornPrices.classes import CornPricesGame

__root = Path(".").absolute()

def initialize_game():
    game_path = __root / "storage" / "game" / f"game.cornprices"
    with open(game_path, 'wb+') as game_file:
        pickle.dump(CornPricesGame(), game_file)

def save_game(game_instance: CornPricesGame):
    game_path = __root / "storage" / "game" / f"game.cornprices"
    with open(game_path, 'wb+') as game_file:
        pickle.dump(game_instance, game_file)

def load_game():
    game_path = __root / "storage" / "game" / f"game.cornprices"
    with open(game_path, 'rb') as game_file:
        game_class = pickle.load(game_file)
    return game_class

def check_environment():
    "Makes sure some important directories and files exist"

    if not path.exists(__root / "storage" / "game"):
        makedirs(__root / "storage" / "game")
        print("Created ./storage/game")

    if not path.exists(__root / "storage" / "game" / "game.cornprices"):
        initialize_game()
        print("Created ./storage/game/game.cornprices")
    
    print("Environment Initialized")

