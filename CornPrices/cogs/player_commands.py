from discord.ext import commands
from discord import Embed
from CornPrices.utils.FileProcessor import load_game, save_game

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cp"])
    async def cornprices(self, ctx):
        "Lists the prices of corn on the market"
        message = Embed(title="Corn Market", description="Prices based upon player interactions, updated every minute", color=0xffff0a)
        game = load_game()
        message.set_thumbnail(url="https://i.kym-cdn.com/entries/icons/mobile/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg")

        for corn_market_tag in game.corn_markets.keys():
            corn_market = game.corn_markets[corn_market_tag]
            message.add_field(name=corn_market.name, value=corn_market.generate_market_listing(), inline=False)
        await ctx.send(embed=message)

    @commands.command(aliases=["w", "money", "m"])
    async def wallet(self, ctx):
        "Displays your net worth"
        game = load_game()
        player = game.get_player(ctx.author.id)

        message = Embed(title="", description=f"Net Worth: ${round(game.get_net_worth_of_player(player),2)}",color=0xffad0a)
        message.add_field(name="Money", value = f"${round(player.money,2)}")

        holdings_string = ""
        for corn_tag in player.corn_holdings.keys():
            holdings_string += f"{game.corn_markets[corn_tag].name}: {player.corn_holdings[corn_tag]}\n"

        if len(holdings_string) > 0:
            message.add_field(name="Corn Holdings", value = holdings_string,inline=False)

        message.set_author(name=f"{ctx.message.author.name}'s wallet", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=message)

    @commands.command(aliases=["b"])
    async def buy(self, ctx, corn_type = "None", amount = 0):
        "Usage: >buy corn-tag amount (leave amount blank to buy max)"
        game = load_game()
        transaction_result = game.do_buy_transaction(ctx.author.id, corn_type, amount)

        # no swtich statements in python
        if transaction_result == "invalid type":
            error_message = Embed(title="Transaction Failed", description="Please input a valid corn tag (type >cp in chat to view a list)")
            await ctx.send(embed=error_message)
        elif transaction_result == "no supply":
            error_message = Embed(title="Transaction Failed", description="There is no more corn of that type avaliable, wait a bit for it to re-stock")
            await ctx.send(embed=error_message)
        elif transaction_result == "not number":
            error_message = Embed(title="Transaction Failed", description="Please input a valid number for the amount you want to buy")
            await ctx.send(embed=error_message)
        elif transaction_result == "below 0":
            error_message = Embed(title="Transaction Failed", description="Please input a valid number above 0")
            await ctx.send(embed=error_message)
        elif transaction_result == "cant buy 1":
            error_message = Embed(title="Transaction Failed", description="You cant afford even a single cob of that type of corn!")
            await ctx.send(embed=error_message)
        elif transaction_result == "buy amount high":
            error_message = Embed(title="Transaction Failed", description="The amount you asked for is more than the amount of corn on the market!")
            await ctx.send(embed=error_message)
        elif transaction_result == "cant buy amount":
            error_message = Embed(title="Transaction Failed", description="You cant afford that much corn, enter a lower amount")
            await ctx.send(embed=error_message)
        else:
            message = Embed(title="Transaction Success", description=transaction_result, color=0x00ff00)
            message.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=message)

        save_game(game)

    @commands.command(aliases=["s"])
    async def sell(self, ctx, corn_type = "None", amount = 0):
        "Usage: >sell corn-tag amount (leave amount blank to sell max)"
        game = load_game()
        transaction_result = game.do_sell_transaction(ctx.author.id, corn_type, amount)
        
        # no swtich statements in python
        if transaction_result == "invalid type":
            error_message = Embed(title="Transaction Failed", description="Please input a valid corn tag (type >cp in chat to view a list)\n You also may not own any of that type of corn!")
            await ctx.send(embed=error_message)
        elif transaction_result == "not number":
            error_message = Embed(title="Transaction Failed", description="Please input a valid number for the amount you want to sell")
            await ctx.send(embed=error_message)
        elif transaction_result == "below 0":
            error_message = Embed(title="Transaction Failed", description="Please input a valid number above 0")
            await ctx.send(embed=error_message)
        else:
            message = Embed(title="Transaction Success", description=transaction_result,color=0x00ff00)
            message.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=message)

        save_game(game)


def setup(bot):
    """setup"""
    bot.add_cog(PlayerCommands(bot))
