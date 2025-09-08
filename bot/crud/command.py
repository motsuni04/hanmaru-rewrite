from discord.ext import commands

from models.command import Command


async def update_command(session, command: commands.Command):
    await session.merge(
        Command(
            name=command.name,
            help=command.help,
            usage=command.usage,
            aliases=command.aliases
        )
    )
    await session.commit()
