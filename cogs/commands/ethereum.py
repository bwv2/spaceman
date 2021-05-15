import discord
from typing import Union
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Ethereum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @cog_ext.cog_subcommand(name='bal',
                            base='eth',
                            guild_ids=[732952864174899230],
                            description='Check the balances of 1 or more ETH addresses.',
                            base_desc='Ethereum-related commands.')
    async def eth_bal(self, ctx: SlashContext, *, addresses: str) -> None:
        if ' ' in (addresses := addresses.strip()):
            addresses = addresses.split()
        if isinstance(addresses, str) and not self.bot.mgr.crypto.eth.is_valid_address(addresses):
            await ctx.send('This is not a **valid ETH address!**')
            return
        if isinstance(addresses, list):
            prev_len: int = len(addresses)
            addresses: Union[list, str] = list(filter(lambda addr: self.bot.mgr.crypto.eth.is_valid_address(addr), addresses))
        if addresses:
            balance: Union[list, str] = await self.bot.mgr.crypto.eth.api.get_address_balance(addresses)
            if not isinstance(addresses, list):
                await ctx.send(content=f'**Balance of** `{addresses}`**:** `{balance}`')
            else:
                embed: discord.Embed = discord.Embed(
                    title='ETH Balances',
                    color=self.bot.mgr.colors.eth,
                    description='\n'.join([f'- `{self.bot.mgr.shorten_address(item.account)}`**:** `{item.balance}`' for item in balance])
                )
                if prev_len > len(addresses):
                    embed.set_footer(text=f'You only see {len(addresses)} balance{"s" if len(addresses) > 1 else ""}, '
                                          f'because some addresses were invalid')
                await ctx.send(embed=embed)
        else:
            await ctx.send('None of the addresses you supplied were **valid!**')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ethereum(bot))
