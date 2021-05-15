import sys
import discord
import traceback
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send('Sorry, this command cannot be ran from DMs!')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Errors(bot))
