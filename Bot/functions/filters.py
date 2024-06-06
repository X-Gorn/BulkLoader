from ..config import Config
from pyrogram import filters


if Config.OWNER_ID:
    OWNER_FILTER = filters.chat(int(Config.OWNER_ID)) & filters.incoming
else:
    OWNER_FILTER = filters.incoming
