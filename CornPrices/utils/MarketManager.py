import asyncio
from CornPrices.utils.FileProcessor import load_game, save_game

async def manage_market(bot):
    await bot.wait_until_ready()
    print("Starting loop")

    while not bot.is_closed():
        game = load_game()

        for corn_tag in game.corn_markets.keys():
            market = game.corn_markets[corn_tag]
            market.update_supply()

        save_game(game)
        await asyncio.sleep(30)