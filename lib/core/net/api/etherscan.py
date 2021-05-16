import aiohttp
from lib.structs import DictProxy
from typing import Tuple, Union, Optional
from urllib.parse import urlencode, unquote

PRECISION: int = 18  # Etherscan returns this many spaces after the comma


class EtherscanAPI:
    def __init__(self, key: str, session: aiohttp.ClientSession):
        self.__key: str = key
        self.ses: aiohttp.ClientSession = session

    def pad_balance(self, balance: str) -> str:
        if len(balance) == PRECISION:
            return f'0.{balance}'
        elif len(balance) < PRECISION:
            return f'0.{"0" * (PRECISION - len(balance))}{balance}'
        else:
            front: str = balance[:-PRECISION]
            back: str = balance.removeprefix(front)
            return f'{front}.{back}'

    async def query(self,
                    module: str,
                    action: str,
                    tag: str = 'latest',
                    method: str = 'get',
                    **kwargs) -> Tuple[bool, DictProxy, Optional[str]]:
        url: str = f'https://api.etherscan.io/api?' + unquote(urlencode(dict(module=module, action=action,
                                                                             tag=tag, apiKey=self.__key,
                                                                             **kwargs)))
        res: aiohttp.ClientResponse = await self.ses.request(method=method, url=url)
        json: DictProxy = DictProxy(await res.json())
        if res.status == 200 and json.message.startswith('OK'):
            return True, json, None
        return False, json, json.result.replace('Error!', '').strip()

    async def get_address_balance(self, address: Union[str, tuple, list]) -> Optional[Union[str, list]]:
        action: str = 'balancemulti' if isinstance(address, (tuple, list)) else 'balance'
        address: str = address if isinstance(address, str) else ','.join(address)
        res: Tuple[bool, DictProxy, Optional[str]] = await self.query(module='account',
                                                                      action=action,
                                                                      address=address)
        if res[0]:
            if isinstance(res[1]['result'], str):
                return self.pad_balance(res[1]['result'])
            else:
                return [DictProxy(account=item.account, balance=self.pad_balance(item.balance)) for item in res[1]['result']]
        return None
