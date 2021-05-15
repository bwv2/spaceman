import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.bot.process_commands(message)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Events(bot))
