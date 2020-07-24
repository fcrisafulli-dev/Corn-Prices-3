import pickle
from os import path, remove, makedirs
from pathlib import Path
from CornPrices.classes import CornPricesGame
from discord import File

__root = Path(".").absolute()
__game_path = __root / "storage" / "game" / f"game.cornprices"
__plot_path = __root / "storage" / "plot" / f"historical_data.png"

def save_plot(plot):
    plot.savefig(__plot_path,bbox_inches="tight")

def get_plot_file():
    "Returns a file in discord's File wrapper named 'historical_data.png'"
    return File(__plot_path, filename="historical_data.png")

def initialize_game():
    with open(__game_path, 'wb+') as game_file:
        pickle.dump(CornPricesGame(), game_file)

def save_game(game_instance: CornPricesGame):
    with open(__game_path, 'wb+') as game_file:
        pickle.dump(game_instance, game_file)

def load_game():
    with open(__game_path, 'rb') as game_file:
        game_class = pickle.load(game_file)
    return game_class

def check_environment():
    "Makes sure some important directories and files exist"

    if not path.exists(__root / "storage" / "game"):
        makedirs(__root / "storage" / "game")
        print("Created ./storage/game")

    if not path.exists(__root / "storage" / "plot"):
        makedirs(__root / "storage" / "plot")
        print("Created ./storage/plot")

    if not path.exists(__game_path):
        initialize_game()
        print("Created ./storage/game/game.cornprices")
    
    print("Environment Initialized")

