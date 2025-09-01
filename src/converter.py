import re

from discord.ext import commands

from src.crud.user import get_user, get_a_user_by_username_ordered_by_level
from src.database import Session


class MaruUserConverter(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.strip()

        async with Session() as session:
            if not argument:
                return await get_user(session, ctx.author.id)

            try:
                user = await commands.MemberConverter().convert(ctx, argument)
                result = await get_user(session, user.id)
                if result:
                    return result
            except commands.MemberNotFound:
                pass

            if (match := re.match(r'^<@!?(\d+)>$', argument)) or argument.isdigit():
                result = await get_user(session, int(match.group(1) if match else argument))
                if result:
                    return result

            result = await get_a_user_by_username_ordered_by_level(session, argument)
            if result:
                return result

        raise commands.UserNotFound(argument)
