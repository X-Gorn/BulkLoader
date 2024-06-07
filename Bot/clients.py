import logging
from .config import Config
from pyrogram import Client, enums


class BotClient(Client):

    def __init__(self):
        self.bot: Client = Client(name='BulkLoader', api_id=Config.APP_ID, api_hash=Config.API_HASH,
                                  bot_token=Config.BOT_TOKEN, plugins=Config.PLUGINS, parse_mode=enums.ParseMode.HTML)
        self.logger: logging.Logger = logging.getLogger('bot')
        self.custom_caption: dict = {}
        self.custom_thumbnail: dict = {}

    async def startup(self):
        await self.bot.start()


client = BotClient()
