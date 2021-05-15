import aiohttp
from . import abc
from lib.core.crypto.currencies.eth import Ethereum


class Crypto:
    def __init__(self, session: aiohttp.ClientSession):
        self.eth = Ethereum(session)
