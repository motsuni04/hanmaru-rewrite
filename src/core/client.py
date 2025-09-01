import os

import discord
from discord.ext import commands

from src import settings
from src.crud.user import register_user
from src.database import Session, init_db


class Maru(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=settings.PREFIXES,
            intents=discord.Intents.default() | discord.Intents(message_content=True),
            case_insensitive=True,
            help_command=None,
            allowed_mentions=discord.AllowedMentions.none(),
            strip_after_prefix=True
        )

    async def setup_hook(self):
        for file in os.listdir('src/ext'):
            if file.endswith('.py'):
                await self.load_extension(f'src.ext.{file[:-3]}')
        await init_db()

    async def on_message(self, message):
        ctx = await self.get_context(message)
        if ctx.command:
            async with Session() as session:
                await register_user(
                    session,
                    ctx.author
                )

            await self.invoke(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.UserNotFound):
            await ctx.reply(
                embed=discord.Embed(
                    description="존재하지 않거나 한마루를 사용하지 않는 사람이에요.",
                    colour=discord.Colour.yellow()
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                embed=discord.Embed(
                    description=f"이 명령어는 {int(error.retry_after + 1)}초 후에 다시 사용할 수 있어요.",
                    colour=discord.Colour.yellow()
                )
            )
        raise error
