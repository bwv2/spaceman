import json
import os
import dotenv
import aiohttp
import dotenv.parser
from colorama import Fore, Style
from typing import Iterator, Union
from lib.core.crypto import Crypto
from lib.structs import DictProxy


class Manager:
    def __init__(self, session: aiohttp.ClientSession):
        self.ses: aiohttp.ClientSession = session
        self.env: DictProxy = DictProxy(dict(os.environ))
        self.crypto: Crypto = Crypto(session)
        self.colors: DictProxy = self.load_json('colors')
        for k, v in self.colors.items():
            if isinstance(v, str):
                self.colors[k] = int(v[1:], 16)
        self.load_dotenv()

    def log(self,
            message: str,
            category: str = 'core',
            bracket_color: Fore = Fore.LIGHTMAGENTA_EX,
            category_color: Fore = Fore.MAGENTA,
            message_color: Fore = Fore.LIGHTWHITE_EX) -> None:
        """
        Colorful logging function because why not.
        :param message: The message to log
        :param category: The text in brackets
        :param bracket_color: The color of the brackets
        :param category_color: The color of the text in the brackets
        :param message_color: The color of the message
        """

        print(f'{bracket_color}[{category_color}{category}{bracket_color}]: {Style.RESET_ALL}{message_color}{message}')

    def load_json(self, name: str) -> DictProxy:
        """
        Load a JSON file from the data dir
        :param name: The name of the JSON file
        :return: The loaded JSON wrapped in DictProxy
        """

        to_load = './data/' + str(name).lower() + '.json' if name[-5:] != '.json' else ''
        with open(to_load, 'r') as fp:
            data: Union[dict, list] = json.load(fp)
        return DictProxy(data)

    def load_dotenv(self):
        """
        Load dotenv contents into self.env with boolean and integer conversions
        """

        with open(dotenv.find_dotenv(), 'r') as fp:
            parsed: Iterator[dotenv.parser.Binding] = dotenv.parser.parse_stream(fp)
            for binding in parsed:
                if binding.value.lower() == 'true':
                    self.env[binding.key] = True
                elif binding.value.lower() == 'false':
                    self.env[binding.key] = False
                elif binding.value.isnumeric():
                    self.env[binding.key] = int(binding.value)
                else:
                    self.env[binding.key] = binding.value

    def shorten_address(self, address: str) -> str:
        chunk: int = int(len(address) / 5)
        front: str = address[:chunk]
        back: str = address[-chunk:]
        return f'{front}...{back}'
