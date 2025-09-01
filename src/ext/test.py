from discord.ext import commands

from src.core.client import Maru
from src.crud.user import get_user, register_user
from src.database import Session


@commands.command(name="가입", aliases=["ㄱㅇ"])
async def register_command(ctx, *, target: commands.MemberConverter = None):
    target = target or ctx.author
    async with Session() as session:
        user = await get_user(session, target.id)
        if user:
            await ctx.reply("이미 가입된 유저입니다.")
            return
        await register_user(
            session,
            discord_id=target.id,
            username=target.global_name
        )
    await ctx.reply("가입이 완료되었습니다.")


async def setup(bot: Maru):
    bot.add_command(register_command)

