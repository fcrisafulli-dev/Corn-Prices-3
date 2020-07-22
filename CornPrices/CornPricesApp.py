from discord.ext import commands
from CornPrices.utils.FileProcessor import check_environment
from CornPrices.utils.MarketManager import manage_market

check_environment()

class CornPricesApp:
    bot = commands.Bot(command_prefix='>')

    bot.load_extension("CornPrices.cogs.player_commands")

    def run(self, secret):
        self.bot.loop.create_task(manage_market(self.bot))
        self.bot.run(secret)