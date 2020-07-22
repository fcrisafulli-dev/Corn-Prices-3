class Corn:
    def __init__(self):
        self.name = "corn"
        self.supply = 0
        self.demand = 0
        self.average_price = 0

    def get_price_change(self):
        return ((self.supply/self.demand) - 2) * -1

    def get_demand_percent(self):
        return ((self.supply/self.demand) - 1) * -100


    def get_price(self):
        return self.average_price * self.get_price_change()

    def generate_market_listing(self):
        price = round(self.get_price(), 2)
        percent = round (self.get_demand_percent(), 1)

        if percent > 0:
            return f"Price: ${price} | Demand: +{percent}%"
        else:
            return f"Price: ${price} | Demand: {percent}%"

class SweetCorn(Corn):
    def __init__(self):
        self.name = "Sweet Corn"
        self.supply = 2_792_135_110
        self.demand = 2_970_357_521
        self.average_price = 4.75

