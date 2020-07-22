from CornPrices.classes.CornTypes import SweetCorn
from CornPrices.classes.Player import Player

class CornPricesGame:
    def __init__(self):
        self.players = {}  # stores player instances 
        self.corn_man = None  # in the future this will be a decleration of an instance of CornMan() 'quest giver'
        
        # stores a discrete amount of corn instances to represent the economy for each type of corn
        self.corn_markets = {
            "sweet-corn" : SweetCorn()
            }

    def get_player(self, pid):
        try:
            return self.players[pid]
        except KeyError:
            self.players[pid] = Player()
            return self.players[pid]

    def do_buy_transaction(self, player_id, corn_type, amount):
        player = self.get_player(player_id)

        corn_tag = corn_type.lower()
        if corn_tag not in self.corn_markets.keys():
            return "invalid type"

        market = self.corn_markets[corn_tag]

        try:
            int(amount)
        except ValueError:
            return "not number"

        if amount < 0:
            return "below 0"

        if player.money < market.get_price():
            return "cant buy 1"

        if int(amount) == 0:
            buy_amount = player.money // market.get_price()
        else:
            buy_amount = int(amount)

        total_price = market.get_price() * buy_amount
        if player.money < total_price:
            return "cant buy amount"

        market.supply -= buy_amount
        player.money -= total_price
        player.add_corn(corn_tag, buy_amount)

        return f"Bought {buy_amount} {market.name} for ${round(total_price,2)}"


        

