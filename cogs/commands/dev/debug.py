import discord
import ast
from discord.ext import commands


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name='dispatch', aliases=['event'])
    async def manually_trigger_event(self, ctx: commands.Context, event: str) -> None:
        event = event.lower().replace('on_', '', 1)
        cor = {
            'guild_join': ctx.guild,
            'guild_remove': ctx.guild,
            'member_join': ctx.author,
            'member_remove': ctx.author
        }
        if cor.get(event, None) is not None:
            e = cor.get(event, None)
            self.bot.dispatch(event, e)
            await ctx.send(f'Dispatched event `{event}`')
        else:
            await ctx.send(f'Failed to dispatch event `{event}`')

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, cmd: str) -> None:
        if ctx.message.author.id == 548803750634979340:
            fn_name = '_eval_expr'

            cmd = cmd.strip('` ')

            cmd = "\n".join(f'    {i}' for i in cmd.splitlines())

            body: str = f'async def {fn_name}():\n{cmd}'

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename='<ast>', mode='exec'), env)  # pylint: disable=exec-used

            result = (await eval(f'{fn_name}()', env))  # pylint: disable=eval-used
            try:
                await ctx.send(result)
            except discord.errors.HTTPException:
                await ctx.send('Evaluation successful, no output.')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Debug(bot))