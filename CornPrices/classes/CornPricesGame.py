from CornPrices.classes.CornTypes import SweetCorn, FunkyCorn, GemCorn
from CornPrices.classes.Player import Player


class CornPricesGame:
    def __init__(self):
        self.players = {}  # stores player instances 
        self.corn_man = None  # in the future this will be a decleration of an instance of CornMan() 'quest giver'
        
        # stores a discrete amount of corn instances to represent the economy for each type of corn
        self.corn_markets = {
            "sweet-corn" : SweetCorn(),
            "funky-corn" : FunkyCorn(),
            "gem-corn" : GemCorn()
            }

    def get_player(self, pid):
        try:
            return self.players[pid]
        except KeyError:
            self.players[pid] = Player()
            return self.players[pid]

    def get_net_worth_of_player(self, player: Player):
        net_w = player.money

        for corn_tag in player.corn_holdings.keys():
            net_w += self.corn_markets[corn_tag].get_price() * player.corn_holdings[corn_tag]

        return net_w

    def do_buy_transaction(self, player_id, corn_type, amount):
        player = self.get_player(player_id)

        corn_tag = corn_type.lower()
        if corn_tag not in self.corn_markets.keys():
            return "invalid type"

        market = self.corn_markets[corn_tag]

        if market.supply < 3:
            return "no supply"

        try:
            int(amount)
        except ValueError:
            return "not number"

        if amount < 0:
            return "below 0"

        if player.money < market.get_price():
            return "cant buy 1"

        if int(amount) == 0:
            buy_amount = 0
            increment = 1
            while True:  # bad way of doing this MUST fix later
                buy_amount += increment
                if player.money > market.get_transaction_price(buy_amount) and buy_amount < market.supply:
                    increment += 1
                else:
                    buy_amount -= increment
                    if increment == 1:
                        break
                    else:
                        increment = 1
        else:
            buy_amount = int(amount)
            if buy_amount > market.supply:
                return "buy amount high"

        total_price = market.get_transaction_price(buy_amount)
        if player.money < total_price:
            return "cant buy amount"

        market.supply -= buy_amount
        player.money -= total_price
        player.add_corn(corn_tag, buy_amount)

        return f"Bought {buy_amount} {market.name} for ${round(total_price,2)}"

    def do_sell_transaction(self, player_id, corn_type, amount):
        player = self.get_player(player_id)

        corn_tag = corn_type.lower()
        if corn_tag not in player.corn_holdings.keys():
            return "invalid type"

        market = self.corn_markets[corn_tag]

        try:
            int(amount)
        except ValueError:
            return "not number"

        if amount < 0:
            return "below 0"

        if int(amount) == 0:
            sell_amount = player.corn_holdings[corn_tag]
        else:
            sell_amount = int(amount)

        total_price = market.get_price() * sell_amount

        market.supply += sell_amount
        player.money += total_price
        player.subtract_corn(corn_tag, sell_amount)

        return f"Sold {sell_amount} {market.name} for ${round(total_price,2)}"

