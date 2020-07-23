class Player:
    def __init__(self):
        self.money = 5000
        self.corn_holdings = {}
        self.name = "Not Found"

    def add_corn(self, corn_tag, amount):
        if corn_tag not in self.corn_holdings.keys():
            self.corn_holdings[corn_tag] = 0

        self.corn_holdings[corn_tag] += amount

    def subtract_corn(self, corn_tag, amount):
        self.corn_holdings[corn_tag] -= amount

        if self.corn_holdings[corn_tag] <= 0:
            del self.corn_holdings[corn_tag]