class Corn:
    def __init__(self):
        self.supply = 0
        self.demand = 0
        self.average_price = 0

    def get_demand_percent(self):
        return ((self.supply/self.demand) - 2) * -1

class SweetCorn(Corn):
    def __init__(self):
        self.supply = 2_792_135_110
        self.demand = 2_970_357_521
        self.average_price = 4.75

