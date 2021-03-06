from discord.ext import commands
from discord import Embed
from CornPrices.utils.FileProcessor import load_game, save_game


class AdminCommands(commands.Cog):
    __admins = [368839778147237890]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update_markets(self, ctx):
        "Used to add new types of corn, only for bot admins"
        if ctx.author.id not in self.__admins:
            return

        message = Embed(title="Preparing to Update", description="Please wait one moment . . .", color=0x000088)
        await ctx.send(embed=message)
        game = load_game()
        game.__init__(game.players)
        save_game(game)
        message = Embed(title="Updated Market", description="Wallets are saved, Corn Market Updated", color=0x0000ff)
        await ctx.send(embed=message)

    @commands.command()
    async def get_price(self, ctx, corn_tag=None):
        "Used to get price of one corn, only for bot admins"
        if ctx.author.id not in self.__admins or not corn_tag:
            return

        game = load_game()
        price = game.corn_markets[corn_tag].get_transaction_price(1)
        message = Embed(title="Listing Price of one", description=f"${round(price,2)}", color=0x0000ff)
        await ctx.send(embed=message)

    @commands.command()
    async def cycle(self, ctx):
        if ctx.author.id not in self.__admins:
            return

        game = load_game()
        message = Embed(title="Running Cycle", description="Please wait one moment . . .", color=0x000088)
        await ctx.send(embed=message)

        for i in range(120):
            for corn_tag in game.corn_markets.keys():
                market = game.corn_markets[corn_tag]
                market.update_supply()
                market.update_history() 

        message = Embed(title="Completed Cycle", description="Corn Market Updated", color=0x0000ff)
        await ctx.send(embed=message)
        save_game(game)

def setup(bot):
    """setup"""
    bot.add_cog(AdminCommands(bot))
