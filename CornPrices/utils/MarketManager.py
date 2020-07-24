import asyncio
from CornPrices.utils.FileProcessor import load_game, save_game
from discord import Streaming
import matplotlib.pyplot as plt
from CornPrices.utils.FileProcessor import save_plot



async def manage_market(bot):
    
    await bot.wait_until_ready()

    print("Starting loop")

    reverse = [(60-(i/2))*-1 for i in range(120)]

    while not bot.is_closed():
        game = load_game()

        plt.clf()
        #plt.style.use('seaborn-darkgrid')
        plt.style.use('dark_background')
        plt.xlabel("Minutes ago")
        plt.ylabel("Demand")

        for corn_tag in game.corn_markets.keys():
            market = game.corn_markets[corn_tag]
            market.update_supply()
            market.update_history() 
            plt.plot(reverse, market.history_data, color=market.display_color, label=market.name)
            
        plt.legend(loc=3)
        save_game(game)
        save_plot(plt)
        await asyncio.sleep(30)