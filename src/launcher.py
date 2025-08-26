import asyncio

import discord

from . import settings
from src.core.client import Maru


async def main():
    bot = Maru()

    async with bot:
        discord.utils.setup_logging()
        await bot.start(settings.TOKEN)


asyncio.run(main())
