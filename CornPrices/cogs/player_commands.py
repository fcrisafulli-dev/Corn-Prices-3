from discord.ext import commands
from discord import Embed
from CornPrices.utils.FileProcessor import load_game, save_game

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cp"])
    async def cornprices(self, ctx):
        message = Embed(title="Corn Market", description="Prices based upon player interactions, updated every minute")
        game = load_game()

        for corn_market_tag in game.corn_markets.keys():
            corn_market = game.corn_markets[corn_market_tag]
            message.add_field(name=corn_market.name, value=corn_market.generate_market_listing())
        await ctx.send(embed=message)

    @commands.command(aliases=["w", "money", "m"])
    async def wallet(self, ctx):
        game = load_game()
        player = game.get_player(ctx.author.id)

        message = Embed(title="Wallet", description=f"Net Worth: ${round(game.get_net_worth_of_player(player),2)}")
        message.add_field(name="Money", value = f"${round(player.money,2)}")

        holdings_string = ""
        for corn_tag in player.corn_holdings.keys():
            holdings_string += f"{game.corn_markets[corn_tag].name}: {player.corn_holdings[corn_tag]}\n"

        if len(holdings_string) > 0:
            message.add_field(name="Corn Holdings", value = holdings_string,inline=False)

        await ctx.send(embed=message)

    @commands.command(aliases=["b"])
    async def buy(self, ctx, corn_type = "None", amount = 0):
        game = load_game()
        transaction_result = game.do_buy_transaction(ctx.author.id, corn_type, amount)

        # no swtich statements in python
        if transaction_result == "invalid type":
            error_message = Embed(title="Transaction Failed", description="Please input a valid corn tag (type >cp in chat to view a list)")
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
        elif transaction_result == "cant buy amount":
            error_message = Embed(title="Transaction Failed", description="You cant afford that much corn, enter a lower amount")
            await ctx.send(embed=error_message)
        else:
            message = Embed(title="Transaction Success", description=transaction_result)
            await ctx.send(embed=message)

        save_game(game)

    @commands.command(aliases=["s"])
    async def sell(self, ctx, corn_type = "None", amount = 0):
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
            message = Embed(title="Transaction Success", description=transaction_result)
            await ctx.send(embed=message)

        save_game(game)


def setup(bot):
    """setup"""
    bot.add_cog(PlayerCommands(bot))
