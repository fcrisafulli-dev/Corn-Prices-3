from discord.ext import commands
from discord import Embed
from CornPrices.utils.FileProcessor import load_game, save_game, get_plot_file

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ct", "corn_top", "corntrop", "t", "corn-top"])
    async def top(self, ctx):
        ": Lists top 10 net worths of players"
        game = load_game()

        player_list = []
        for pid in game.players.keys():
            user = await self.bot.fetch_user(pid)
            game.players[pid].name = user.name
            player_list.append(game.players[pid])

        player_list.sort(key=lambda plr: game.get_net_worth_of_player(plr), reverse=True)

        message = Embed(title="Top Players", description="Top 10 players with the highest net worths", color=0xffff0a)
        for i in range(min(10, len(player_list))):
            message.add_field(name=player_list[i].name,
            value=f"Net Worth: ${'{:,.2f}'.format(game.get_net_worth_of_player(player_list[i]))}",inline=False)

        await ctx.send(embed=message)
        

    @commands.command(aliases=["cp"])
    async def cornprices(self, ctx):
        "Lists the prices of corn on the market"
        message = Embed(title="Corn Market", description="Prices based upon player interactions, updated every minute", color=0xffff0a)
        game = load_game()
        message.set_thumbnail(url="https://i.kym-cdn.com/entries/icons/mobile/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg")

        for corn_market_tag in game.corn_markets.keys():
            corn_market = game.corn_markets[corn_market_tag]
            message.add_field(name=corn_market.name, value=corn_market.generate_market_listing(), inline=False)

        message.set_image(url="attachment://historical_data.png")
        await ctx.send(file=get_plot_file(), embed=message)

    @commands.command(aliases=["w", "money", "m"])
    async def wallet(self, ctx):
        "Displays your net worth"
        game = load_game()
        player = game.get_player(ctx.author.id)

        message = Embed(title="", description=f"Net Worth: ${'{:,.2f}'.format(game.get_net_worth_of_player(player))}",color=0xffad0a)
        message.add_field(name="Money", value = f"${'{:,.2f}'.format(player.money)}")

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

    @commands.command(aliases=["i"])
    async def info(self, ctx, corn_type = "None"):
        game = load_game()

        corn_tag = corn_type.lower()
        if corn_tag not in game.corn_markets.keys():
            error_message = Embed(title="Cannot Display Info", 
                description="Please input a valid corn tag (type >cp in chat to view a list)")
            await ctx.send(embed=error_message)
            return

        market = game.corn_markets[corn_tag]

        buyout = market.get_transaction_price(market.supply)

        message = Embed(title=f"Information on {market.name}", 
            description=f"Buyout value: ${'{:,.2f}'.format(buyout)}\nStable average price: ${market.average_price}",
            color=0x0000ff)
        await ctx.send(embed=message)

    @commands.command(aliases=["p"])
    async def pay(self, ctx, Mention = "", amount = ""):
        game = load_game()
        try:
            reciever = game.get_player(ctx.message.mentions[0].id)
            sender = game.get_player(ctx.message.author.id)
        except IndexError:
            message = Embed(title=f"Transaction Failed", 
            description=f"No mention was included, or the user is not in this server",
            color=0xff0000)
            await ctx.send(embed=message)
            return

        try:
            dollars = float(amount)
        except ValueError:
            message = Embed(title=f"Transaction Failed", 
            description=f"You must enter an amount greater than 0",
            color=0xff0000)
            await ctx.send(embed=message)
            return

        if dollars <= 0:
            message = Embed(title=f"Transaction Failed", 
            description=f"You must enter an amount greater than 0",
            color=0xff0000)
            await ctx.send(embed=message)
            return

        if dollars > sender.money:
            message = Embed(title=f"Transaction Failed", 
            description=f"You do not have that much money!",
            color=0xff0000)
            await ctx.send(embed=message)
            return


        sender.money -= dollars
        reciever.money += dollars

        save_game(game)

        message = Embed(title=f"Transaction Completed", 
            description=f"{ctx.message.author.name} sent {ctx.message.mentions[0].name} ${'{:,.2f}'.format(dollars)}",
            color=0x00ff00)
        await ctx.send(embed=message)

     




def setup(bot):
    """setup"""
    bot.add_cog(PlayerCommands(bot))
