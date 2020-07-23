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


def setup(bot):
    """setup"""
    bot.add_cog(AdminCommands(bot))
