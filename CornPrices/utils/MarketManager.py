import asyncio
from random import uniform
from CornPrices.utils.FileProcessor import load_game, save_game

async def manage_market(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        game = load_game()
        for corn_tag in game.corn_markets.keys():
            market = game.corn_markets[corn_tag]
            demand = market.get_demand_percent()
            if abs(demand) > 18:
                amount_change = uniform(.02,.07) * market.supply
                if demand > 0:
                    market.supply += amount_change
                else:
                    market.supply -= amount_change
            else:
                amount_change = uniform(-.052,.052) * market.supply
                market.supply += amount_change
        save_game(game)
        await asyncio.sleep(30)