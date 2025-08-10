import asyncio

import discord

from . import settings
from src.core.client import Maru


async def main():
    bot = Maru()

    @bot.command(name="테스트", aliases=["ㅌㅅㅌ"])
    async def test_command(ctx):
        await ctx.send("테스트")

    async with bot:
        discord.utils.setup_logging()
        await bot.start(settings.TOKEN)


asyncio.run(main())
