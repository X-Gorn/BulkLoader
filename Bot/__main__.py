from . import client
from pyrogram import idle
from .config import Config
import os


async def main():
    await client.startup()
    await client.bot.set_bot_commands(commands=Config.BOT_COMMANDS)
    client.logger.info('Bot Started')
    await idle()


if __name__ == '__main__':
    if not os.path.isdir(Config.DOWNLOAD_DIR):
        os.makedirs(Config.DOWNLOAD_DIR)
    client.run(main())
