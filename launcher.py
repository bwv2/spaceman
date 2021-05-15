import os
import asyncio
from dotenv import load_dotenv
from bot import Spaceman

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

load_dotenv()


def main() -> None:
    bot: Spaceman = Spaceman()
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
