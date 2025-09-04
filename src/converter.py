import re

from discord.ext import commands

from src.crud.user import get_user, get_a_user_by_username_ordered_by_level
from src.database import Session
from src.utils import unitize


class BetConverter(commands.Converter):
    all_in = ("올인", "all", '전부', '모두', 'ㅇㅇ', 'ㅈㅂ', 'ㅁㄷ')

    def __init__(self, min_bet=100, max_bet=1_000_000):
        super().__init__()
        self.min_bet = min_bet
        self.max_bet = max_bet

    async def convert(self, ctx, argument):
        has = (await get_user(Session(), ctx.author.id)).token
        try:
            if argument in BetConverter.all_in:
                amount = min(has, self.max_bet)
            else:
                amount = int(argument)

            if has < amount:
                raise commands.BadArgument(
                    f"가지고 있는 토큰이 부족해요. ({unitize(has)}개 보유 중)"
                )
            elif amount < self.min_bet or amount > self.max_bet:
                raise commands.BadArgument(
                    f"베팅할 토큰 개수는 {unitize(self.min_bet)} ~ {unitize(self.max_bet)}개 사이어야 해요."
                )
            return amount
        except ValueError:
            raise commands.BadArgument("유효한 숫자를 입력해주세요.")


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
