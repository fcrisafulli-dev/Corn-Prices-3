from discord.ext import commands
from discord import Embed

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cornprices(self, ctx):
        message = Embed(title="Title", description="description")
        await ctx.send(embed=message)


def setup(bot):
    """setup"""
    bot.add_cog(PlayerCommands(bot))
