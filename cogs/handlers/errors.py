import sys
import discord
import traceback
from colorama import Fore
from discord.ext import commands
from discord_slash import SlashContext


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
                self.bot.mgr.log(f'In {ctx.command.qualified_name}:',
                                 category='error',
                                 bracket_color=Fore.LIGHTRED_EX,
                                 category_color=Fore.RED,
                                 message_color=Fore.LIGHTRED_EX,
                                 file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                self.bot.mgr.log(f'{original.__class__.__name__}: {original}',
                                 category='error',
                                 bracket_color=Fore.LIGHTRED_EX,
                                 category_color=Fore.RED,
                                 message_color=Fore.LIGHTRED_EX,
                                 file=sys.stderr)
        elif not self.bot.mgr.env.production:
            raise error

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, error) -> None:
        embed = discord.Embed(title="An error has occured!", color=discord.Color.red())
        embed.add_field(name='Full Traceback',
                        value=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\n```",
                        inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Errors(bot))
