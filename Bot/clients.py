import logging
from .config import Config
from pyrogram import Client


class BotClient(Client):

    def __init__(self):
        self.bot: Client = Client(name='BulkLoader', api_id=Config.APP_ID, api_hash=Config.API_HASH,
                                  bot_token=Config.BOT_TOKEN, plugins=Config.PLUGINS)
        self.logger: logging.Logger = logging.getLogger('bot')

    async def startup(self):
        await self.bot.start()


client = BotClient()
