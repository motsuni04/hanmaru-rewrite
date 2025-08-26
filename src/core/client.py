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
                    ctx.author.id,
                    ctx.author.global_name
                )

            await self.invoke(ctx)

    async def on_command_error(self, ctx, error):
        raise error
