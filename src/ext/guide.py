import discord
from discord.ext import commands

from src.core.client import Maru
from src.emojis import MARU, TOKEN


class GuideView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="공식 서버",
                emoji=MARU,
                style=discord.ButtonStyle.link,
                url="https://discord.gg/tTq9aD3"
            )
        )


@commands.command(
    name="도움", aliases=["ㄷㅇ", "명령어", "ㅁㄹㅇ", "커맨드", "ㅋㅁㄷ", "헬프", "ㅎㅍ", "도움말", "ㄷㅇㅁ"]
)
@commands.cooldown(1, 2, commands.BucketType.user)
async def guide(ctx):
    def to_linked(cmd: str) -> str:
        return f'[{cmd}]({"https://hanmaru.tech/commands/" + cmd})'

    prefix = ctx.clean_prefix
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title="도움말",
        description=(
            f"- **{prefix}{to_linked('정보')}**: 가지고 있는 토큰을 확인해요.\n"
            f"- **{prefix}{to_linked('토큰')}**: 토큰을 얻어요. 1분마다 사용할 수 있어요.\n"
            f"- **{prefix}{to_linked('출석')}**: 출석 보상을 받아요.\n"
            f"- **{prefix}{to_linked('가위바위보')} [베팅]**: 가위바위보 게임을 해요.\n"
        )
    )

    extra_commands = "통계 끝말잇기 요트다이스 슬롯 바카라 블랙잭 뭐먹지 가방 업적 알림 랭킹".split()
    embed.add_field(
        name="모든 명령어",
        value=' '.join(map(to_linked, extra_commands))
    )
    await ctx.reply(
        embed=embed, view=GuideView()
    )


async def setup(bot: Maru):
    bot.add_command(guide)  # noqa
