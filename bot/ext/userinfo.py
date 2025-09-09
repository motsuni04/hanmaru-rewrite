import discord
from discord.ext import commands

from converter import MaruUserConverter
from core.client import Maru
from emojis import TOKEN
from utils import get_max_exp, unitize


@commands.command(
    name="정보", aliases=["ㅈㅂ"], rest_is_raw=True,
    usage="{prefix}정보 <유저>\n"
          "- 내 정보를 보려면: {prefix}정보\n"
          "- 한마루의 정보를 보려면: {prefix}정보 한마루  /  {prefix}정보 @한마루"
)
@commands.cooldown(1, 1, commands.BucketType.user)
async def userinfo(ctx, *, target: MaruUserConverter()):
    """
나 또는 다른 사람의 정보를 확인해요.
    """
    min_exp = get_max_exp(target.level - 1)
    max_exp = get_max_exp(target.level)
    progress = target.exp - min_exp
    goal = max_exp - min_exp

    embed = discord.Embed(
        colour=discord.Colour.green(),
        title=target.username,
        description=f"Lv.**{target.level:,}** {target.title}\n"
                    f"-# {progress:,} / {goal:,}  ({progress / goal * 100:.1f}%)\n\n"
                    f"**{TOKEN} 토큰** {unitize(target.token)}\n"
                    f"**<:star:1411929160345371651> 스타** {unitize(target.star)}"
    )
    embed.set_thumbnail(url=target.avatar_url)
    await ctx.send(embed=embed)


async def setup(bot: Maru):
    bot.add_command(userinfo)  # noqa
