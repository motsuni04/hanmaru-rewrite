import discord
from discord.ext import commands

from src.converter import MaruUserConverter
from src.core.client import Maru
from src.utils import get_max_exp, unitize


@commands.command(name="정보", aliases=["ㅈㅂ"], rest_is_raw=True)
@commands.cooldown(1, 1, commands.BucketType.user)
async def userinfo(ctx, *, target: MaruUserConverter()):
    min_exp = get_max_exp(target.level - 1)
    max_exp = get_max_exp(target.level)
    embed = discord.Embed(
        colour=discord.Colour.green(),
        title=target.username,
        description=f"Lv.**{target.level:,}** {target.title}\n"
                    f"-# {target.exp - min_exp:,} / {max_exp - min_exp:,}\n\n"
                    f"**<:token:1411929162616275056> 토큰** {unitize(target.token)}\n"
                    f"**<:star:1411929160345371651> 스타** {unitize(target.star)}"
    )
    embed.set_thumbnail(url=target.avatar_url)
    await ctx.send(embed=embed)


async def setup(bot: Maru):
    bot.add_command(userinfo)
