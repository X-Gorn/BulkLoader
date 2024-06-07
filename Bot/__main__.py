from . import client
from pyrogram import idle
from .config import Config


async def main():
    await client.startup()
    await client.bot.set_bot_commands(commands=Config.BOT_COMMANDS)
    client.logger.info('Bot Started')
    await idle()


if __name__ == '__main__':
    client.run(main())
