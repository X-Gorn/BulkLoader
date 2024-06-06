from . import client
from pyrogram import idle


async def main():
    await client.startup()
    client.logger.info('Bot Started')
    await idle()


if __name__ == '__main__':
    client.run(main())
