import asyncio
import random

import discord
from discord.ext import commands

from src.converter import BetConverter
from src.core.client import Maru
from src.crud.user import get_user, add_token
from src.database import Session
from src.emojis import TOKEN, RPS, ROCK, SCISSOR, PAPER
from src.utils import unitize
from src.views import MyView


MIN_BET = 100
MAX_BET = 1_000_000


class RPSContinueButton(discord.ui.Button):
    def __init__(self, bet, rate):
        self.rate = rate
        super().__init__(
            style=discord.ButtonStyle.green,
            label=f"계속하기 ({unitize(bet)})"
        )

    async def callback(self, interaction: discord.Interaction):
        view: RPSContinueView = self.view
        await view.set_result(interaction, self.rate)

class RPSDoubleButton(discord.ui.Button):
    def __init__(self, init_bet, rate):
        self.rate = rate
        next_bet = int(init_bet * pow(2, rate + 1))
        super().__init__(
            style=discord.ButtonStyle.red,
            label=f"더블업 ({unitize(next_bet)})"
        )

    async def callback(self, interaction: discord.Interaction):
        view: RPSContinueView = self.view
        await view.set_result(interaction, self.rate + 1)


class RPSHalfButton(discord.ui.Button):
    def __init__(self, bet, rate):
        self.rate = rate
        super().__init__(
            style=discord.ButtonStyle.gray,
            label=f"하프 ({unitize(bet // 2)})"
        )

    async def callback(self, interaction: discord.Interaction):
        view: RPSContinueView = self.view
        await view.set_result(interaction, self.rate - 1)


class RPSContinueView(MyView):
    def __init__(self, has, ctx, bet, init_bet, rate, can_double=True):
        super().__init__(ctx, timeout=20)
        self.bet = bet
        self.init_bet = init_bet
        self.rate = rate
        self.value = None
        if has >= self.bet:
            self.add_item(RPSContinueButton(self.bet, self.rate))
        double_bet = int(self.init_bet * pow(2, self.rate + 1))
        if can_double and has >= double_bet:
            self.add_item(RPSDoubleButton(self.init_bet, self.rate))
        if has >= self.bet // 2 >= MIN_BET:
            self.add_item(RPSHalfButton(self.bet, self.rate))
        if not self.children:
            self.add_item(discord.ui.Button(
                style=discord.ButtonStyle.gray,
                label="토큰이 부족해서 계속할 수 없어요.",
                disabled=True
            ))
            self.stop()

    async def set_result(self, interaction: discord.Interaction, value):
        self.value = value
        asyncio.create_task(interaction.response.edit_message(view=None))
        self.stop()


class RPSGameView(MyView):
    def __init__(self, ctx, bet, init_bet, rate):
        super().__init__(ctx, timeout=30)
        self.bet = bet
        self.init_bet = init_bet
        self.rate = rate
        self.dealer = random.randint(0, 2)
        self.select = None
        self.followup = None

    @property
    def result(self):
        if self.select is None:
            return None
        return (self.select - self.dealer) % 3

    @property
    def reward(self):
        return (1, 2, 0)[self.result or 0]

    async def display_result(self, interaction: discord.Interaction):
        result_color = (discord.Colour.light_gray(), discord.Colour.green(), discord.Colour.red())[self.result]
        result_content = (
            "무승부!",
            f"이겼어요! + {TOKEN} **{unitize(self.bet * 2)}**",
            "졌어요.."
        )[self.result]
        result_embed = discord.Embed(colour=result_color, description=result_content)
        moves = (SCISSOR, ROCK, PAPER)

        next_bet = self.bet
        next_rate = self.rate
        can_double = True
        if self.result == 2:
            while (next_bet := int(self.init_bet * pow(2, next_rate))) > MAX_BET:
                next_rate -= 1
            can_double = next_rate == self.rate

        async with Session() as session:
            has = (await get_user(session, self.ctx.author.id)).token + (self.bet * self.reward)

        self.followup = RPSContinueView(
            has, self.ctx, next_bet, self.init_bet, next_rate,
            can_double=can_double
        )
        self.followup.message = self.message
        await interaction.response.edit_message(
            content=f"{self.ctx.author.global_name} {moves[self.select]} 🆚 {moves[self.dealer]} 한마루\n"
                    f"-# 베팅: {TOKEN} **{unitize(self.bet)}**",
            view=self.followup,
            embed=result_embed
        )
        self.stop()

    @discord.ui.button(emoji=SCISSOR, style=discord.ButtonStyle.gray)
    async def scissor(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.select = 0
        await self.display_result(interaction)

    @discord.ui.button(emoji=ROCK, style=discord.ButtonStyle.gray)
    async def rock(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.select = 1
        await self.display_result(interaction)

    @discord.ui.button(emoji=PAPER, style=discord.ButtonStyle.gray)
    async def paper(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.select = 2
        await self.display_result(interaction)


@commands.command(
    name="가위바위보", aliases=["ㄱㅇㅂㅇㅂ"],
    usage="{prefix}가위바위보 [배팅]\n"
          f"- 100 {TOKEN}을 베팅하려면 "
          "**{prefix}가위바위보 100**"
)
@commands.cooldown(1, 3, commands.BucketType.user)
async def rps(ctx, *, init_bet: BetConverter(MIN_BET, MAX_BET)):
    rate = 0
    async with Session() as session:
        while True:
            bet = int(init_bet * pow(2, rate))
            ok = await add_token(session, ctx.author.id, -bet)
            if not ok:
                has = (await get_user(session, ctx.author.id)).token
                await ctx.send(
                    f"가지고 있는 토큰이 부족해요. ({unitize(has)}개 보유 중)"
                )
                return

            game_view = RPSGameView(ctx, bet, init_bet, rate)
            game_view.message = await ctx.send(
                f"{ctx.author.display_name} {RPS} 🆚 {RPS} 한마루\n"
                f"-# 베팅: {TOKEN} **{unitize(bet)}**",
                view=game_view
            )
            timeout = await game_view.wait()
            reward = game_view.reward
            if reward:
                await add_token(session, ctx.author.id, bet * reward)
            if timeout:
                await game_view.message.edit(content="시간이 초과되어 취소되었어요.")
                return
            if not game_view.followup:
                return
            await game_view.followup.wait()
            if game_view.followup.value is None:
                return
            rate = game_view.followup.value



async def setup(bot: Maru):
    bot.add_command(rps)  # noqa
