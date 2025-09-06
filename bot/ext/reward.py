import random
from discord.ext import commands

from core.client import Maru
from crud.user import add_token
from database import Session
from emojis import TOKEN
from utils import unitize


@commands.command(
    name="토큰", aliases=["ㅌㅋ", "돈줘", "ㄷㅈ", "돈"]
)
@commands.cooldown(1, 60, commands.BucketType.user)
async def reward(ctx):
    count = 4000 + 500 * random.randint(3, 16)

    await ctx.reply(
        random.choice((
            "토큰 {icon} **{count}**개 획득!",
            "토큰을 받았어요! {icon} +**{count}**",
            "{icon} **{count}**개가 주머니에 쏙!",
            "토큰을 드릴게요.. 이번엔 {icon} +**{count}**개!",
        )).format(icon=TOKEN, count=unitize(count))
    )
    async with Session() as session:
        await add_token(session, ctx.author.id, count)


async def setup(bot: Maru):
    bot.add_command(reward)
