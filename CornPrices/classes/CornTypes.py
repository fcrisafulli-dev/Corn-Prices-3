from random import uniform

class Corn:
    def __init__(self):
        self.name = "corn"
        self.tag = "corn"
        self.supply = 0
        self.demand = 0
        self.average_price = 0

        self.history_data = [0 for i in range(60)]
        self.display_color = "black"

    def get_price_change(self):
        return ((self.supply/self.demand) - 2) * -1

    def get_demand_percent(self):
        return ((self.supply/self.demand) - 1) * -100

    def get_price(self):
        return self.average_price * self.get_price_change()

    def predict_percent_change(self, amount):
        original = self.get_price()
        new = self.average_price * ((((self.supply+amount)/self.demand) - 2) * -1)

        return ((new/original) - 2) * -1

    def get_transaction_price(self, amount):
        return self.average_price * amount * self.predict_percent_change(amount)

    def generate_market_listing(self):
        price = round(self.get_price(), 2)
        percent = round (self.get_demand_percent(), 1)

        if percent > 0:
            return f"Price: ${price} | Demand: +{percent}% \nTag: {self.tag}"
        else:
            return f"Price: ${price} | Demand: {percent}% \nTag: {self.tag}"

    def update_history(self):
        self.history_data.append(self.get_demand_percent())
        self.history_data = self.history_data[-60:]

    def update_supply(self):
        demand = self.get_demand_percent()
        if abs(demand) > 18:
            amount_change = uniform(.02,.07) * self.demand
            if demand > 0:
                self.supply += amount_change
            else:
                self.supply -= amount_change
        else:
            amount_change = uniform(-.052,.052) * self.demand
            self.supply += amount_change


class SweetCorn(Corn):
    def __init__(self):
        super().__init__()
        self.name = "Sweet Corn"
        self.tag = "sweet-corn"
        self.supply = 1_970_357_521
        self.demand = 1_970_357_521
        self.average_price = 4.75

        self.display_color = "goldenrod"


class FunkyCorn(Corn):
    def __init__(self):
        super().__init__()
        self.name = "Funky Corn"
        self.tag = "funky-corn"
        self.supply = 0
        self.demand = 900_000_000
        self.average_price = 15.43

        self.display_color = "purple"

        self.climb = "supply"

    def update_supply(self):
        demand = self.get_demand_percent()

        if demand > 80:
            amount_change = uniform(-.005,.010) * self.demand
            self.supply += amount_change
        
        else:
            if self.climb == "supply":  # decreases demand
                amount_change = uniform(.01,.04) * self.demand
                self.supply += amount_change
                if self.supply > self.demand and uniform(0,100) < 10:
                    self.climb = "demand"

            elif self.climb == "demand":
                amount_change = uniform(.03,.15) * self.demand
                self.supply -= amount_change
                if self.supply < self.demand and uniform(0,100) < 40:
                    self.climb = "supply"


class GemCorn(Corn):
    def __init__(self):
        super().__init__()
        self.name = "Gem Corn"
        self.tag = "gem-corn"
        self.supply = 4_000_000
        self.demand = 2_000_000
        self.average_price = 9000.05

        self.display_color = "dodgerblue"

    def update_supply(self):
        demand = self.get_demand_percent()
        if demand < 25:
            amount_change = uniform(-.02,.04) * self.demand
            self.supply -= amount_change
        else:
            if uniform(0,100) < 10:
                amount_change = uniform(.10,.30) * self.demand
            else:
                amount_change = uniform(-.02,.02) * self.demand
            self.supply += amount_change
