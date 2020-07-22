from discord.ext import commands
from discord import Embed
from CornPrices.utils.FileProcessor import load_game

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cornprices(self, ctx):
        message = Embed(title="Corn Market", description="Prices based upon player interactions, updated every minute")

        game = load_game()

        for corn_market in game.corn_markets:
            message.add_field(name=corn_market.name, value=corn_market.generate_market_listing())

        await ctx.send(embed=message)


def setup(bot):
    """setup"""
    bot.add_cog(PlayerCommands(bot))
