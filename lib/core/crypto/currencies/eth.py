import os
import aiohttp
import re
from lib.core.crypto.abc import Currency
from typing import Union
from lib.core.net.api.etherscan import EtherscanAPI


class Ethereum(Currency):
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__('eth')
        self.pattern: re.Pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
        self.api: EtherscanAPI = EtherscanAPI(os.getenv('ETHERSCAN_TOKEN'), session)

    def is_valid_address(self, address: Union[bytes, str]) -> bool:
        return bool(re.match(self.pattern, address))
