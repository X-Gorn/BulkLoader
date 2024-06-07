from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from functions.filters import OWNER_FILTER


reply_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Source", url="https://github.com/X-Gorn/BulkLoader"),
        InlineKeyboardButton(text="LinkTree", url="https://xgorn.is-a.dev"),
    ],
    [InlineKeyboardButton(text="Author", url="https://t.me/xgorn")],
])


@Client.on_message(filters.command('start') & OWNER_FILTER & filters.private)
async def start(bot: Client, update: Message):
    await update.reply_text(text=f"I'm BulkLoader\nYou can upload list of urls\n\n/help for more details!", quote=True, reply_markup=reply_markup)


@Client.on_message(filters.command('help') & OWNER_FILTER & filters.private)
async def help(bot: Client, update: Message):
    await update.reply_text(text=f"How to use BulkLoader?!\n\n2 Methods:\n- send command /link and then send urls, separated by new line.\n- send txt file (links), separated by new line.", quote=True, reply_markup=reply_markup)
