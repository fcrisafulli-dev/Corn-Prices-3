import asyncio
from CornPrices.utils.FileProcessor import load_game, save_game
from discord import Streaming

async def manage_market(bot):
    
    await bot.wait_until_ready()

    print("Starting loop")

    while not bot.is_closed():
        await bot.change_presence(activity=Streaming(name="gathering corn prices", url="https://images-ext-2.discordapp.net/external/amuYA__rRHx932sbBXdu4RzVsOwNgqPMte7gBV-zOow/https/i.kym-cdn.com/entries/icons/mobile/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg"))
        game = load_game()

        for corn_tag in game.corn_markets.keys():
            market = game.corn_markets[corn_tag]
            market.update_supply()

        save_game(game)
        await asyncio.sleep(5)
        await bot.change_presence(activity=Streaming(name="fresh corn prices", url="https://images-ext-2.discordapp.net/external/amuYA__rRHx932sbBXdu4RzVsOwNgqPMte7gBV-zOow/https/i.kym-cdn.com/entries/icons/mobile/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg"))
        await asyncio.sleep(55)