import discord
from discord.ext import commands

from src import settings


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
