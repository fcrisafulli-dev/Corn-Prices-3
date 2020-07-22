from discord.ext import commands
from CornPrices.utils.FileProcessor import check_environment

check_environment()

class CornPricesApp:
    bot = commands.Bot(command_prefix='>')

    bot.load_extension("CornPrices.cogs.player_commands")

    def run(self, secret):
        self.bot.run(secret)