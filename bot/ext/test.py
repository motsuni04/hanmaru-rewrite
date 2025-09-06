from discord.ext import commands

from core.client import Maru
from crud.user import get_user, register_user
from database import Session


@commands.command(name="가입", aliases=["ㄱㅇ"])
@commands.is_owner()
async def register_command(ctx, *, target: commands.MemberConverter = None):
    target = target or ctx.author
    async with Session() as session:
        user = await get_user(session, target.id)
        if user:
            await ctx.reply("이미 가입된 유저입니다.")
            return
        await register_user(
            session,
            target
        )
    await ctx.reply("가입이 완료되었습니다.")


async def setup(bot: Maru):
    bot.add_command(register_command)

