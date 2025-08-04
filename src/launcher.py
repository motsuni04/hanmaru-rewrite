import asyncio

import discord
from discord.ext import commands


async def main():
    bot = commands.AutoShardedBot(command_prefix='ㅎ')
    async with bot:
        discord.utils.setup_logging()
        # await bot.start(TOKEN)


asyncio.run(main())
