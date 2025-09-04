import asyncio

import discord


class MyView(discord.ui.View):
    def __init__(self, ctx, timeout=30):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.message = None

    async def cleanup(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    async def on_timeout(self):
        await self.cleanup()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            asyncio.create_task(
                interaction.response.send_message(
                    "사용할 수 없는 내용이에요.", ephemeral=True
                )
            )
            return False
        return True