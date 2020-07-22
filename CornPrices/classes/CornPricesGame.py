from CornPrices.classes.CornTypes import SweetCorn

class CornPricesGame:
    def __init__(self):
        self.players = []  # stores player instances 
        self.corn_man = None  # in the future this will be a decleration of an instance of CornMan() 'quest giver'
        
        # stores a discrete amount of corn instances to represent the economy for each type of corn
        self.corn_markets = [SweetCorn()]