from discord.ext import commands

from src.core.client import Maru
from src.crud.user import get_user, register_user
from src.database import Session


@commands.command(name="가입", aliases=["ㄱㅇ"])
async def register_command(ctx):
    async with Session() as session:
        user = await get_user(session, ctx.author.id)
        if user:
            await ctx.reply("이미 가입된 유저입니다.")
            return
        await register_user(
            session,
            discord_id=ctx.author.id,
            username=ctx.author.global_name
        )
    await ctx.reply("가입이 완료되었습니다.")


@commands.command(name="정보", aliases=["ㅈㅂ"])
async def test_command(ctx, *, target: commands.MemberConverter = None):
    async with Session() as session:
        user = await get_user(session, (target or ctx.author).id)
        if user is None:
            await ctx.send("유저가 없습니다.")
        else:
            await ctx.send(f"유저 {user.username}의 토큰: {user.token}")


async def setup(bot: Maru):
    bot.add_command(register_command)
    bot.add_command(test_command)

