import os
import time
import shutil
import asyncio
import traceback
from functions.filters import OWNER_FILTER
from functions.helper import progress_for_pyrogram, download_file, absolute_paths, send_media, URL_REGEX, CALLBACK_REGEX
from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import BadRequest, FloodWait
from .. import client


CB_BUTTONS = [
    [
        InlineKeyboardButton(text="Zip", callback_data="zip"),
        InlineKeyboardButton(text="One by one", callback_data="1by1"),
    ]
]


@Client.on_message(filters.command('link') & OWNER_FILTER & filters.private)
async def linkloader(bot: Client, update: Message):
    xlink = await update.chat.ask('Send links to download.', filters=filters.text, timeout=300)
    if Config.BUTTONS:
        return await xlink.reply('Choose method to upload file.', True, reply_markup=InlineKeyboardMarkup(CB_BUTTONS))
    dirs = f'downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    output_filename = str(update.from_user.id)
    filename = f'{dirs}/{output_filename}.zip'
    pablo = await update.reply_text('Downloading...')
    urls = URL_REGEX.findall(xlink.text)
    rm, total, up = len(urls), len(urls), 0
    await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
    for url in urls:
        await download_file(url, dirs)
        up += 1
        rm -= 1
        try:
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except FloodWait as e:
            client.logger.warning(
                'Floodwait for {} seconds'.format(e.value))
            await asyncio.sleep(e.value)
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except Exception:
            client.logger.warning(traceback.format_exc())
    await pablo.edit_text('Uploading...')
    if Config.AS_ZIP:
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=(
                'Uploading...',
                pablo,
                start_time
            )
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    else:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for files in dldirs:
            await send_media(files, pablo)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@Client.on_message(filters.document & OWNER_FILTER & filters.private)
async def loader(bot: Client, update: Message):
    if Config.BUTTONS:
        return await update.reply('Choose method to upload file.', True, reply_markup=InlineKeyboardMarkup(CB_BUTTONS))
    dirs = f'downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not update.document.file_name.endswith('.txt'):
        return
    output_filename = update.document.file_name[:-4]
    filename = f'{dirs}/{output_filename}.zip'
    pablo = await update.reply_text('Downloading...')
    fl = await update.download()
    with open(fl) as f:
        urls = URL_REGEX.findall(f.read())
    rm, total, up = len(urls), len(urls), 0
    await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
    for url in urls:
        await download_file(url, dirs)
        up += 1
        rm -= 1
        try:
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except FloodWait as e:
            client.logger.warning(
                'Floodwait for {} seconds'.format(e.value))
            await asyncio.sleep(e.value)
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except Exception:
            client.logger.warning(traceback.format_exc())
    await pablo.edit_text('Uploading...')
    os.remove(fl)
    if Config.AS_ZIP:
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        try:
            await update.reply_document(
                filename,
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await update.reply_document(
                filename,
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except Exception:
            client.logger.warning(traceback.format_exc())
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    else:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for media in dldirs:
            try:
                await send_media(media, pablo)
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await send_media(media, pablo)
            except Exception:
                client.logger.warning(traceback.format_exc())
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@Client.on_callback_query(filters.regex(pattern=CALLBACK_REGEX))
async def callbacks(bot: Client, update: CallbackQuery):
    await update.message.delete()
    dirs = f'downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if update.message.reply_to_message.document:
        output_filename = update.message.reply_to_message.document.file_name[:-4]
        filename = f'{dirs}/{output_filename}.zip'
        pablo = await update.message.reply_to_message.reply_text('Downloading...')
        fl = await update.message.reply_to_message.download()
        with open(fl) as f:
            urls = URL_REGEX.findall(f.read())
        rm, total, up = len(urls), len(urls), 0
        await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        for url in urls:
            await download_file(url, dirs)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
        os.remove(fl)
    elif update.message.reply_to_message.text:
        output_filename = str(update.message.reply_to_message.from_user.id)
        filename = f'{dirs}/{output_filename}.zip'
        pablo = await update.message.reply_to_message.reply_text('Downloading...')
        urls = URL_REGEX.findall(update.message.reply_to_message.text)
        rm, total, up = len(urls), len(urls), 0
        await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        for url in urls:
            await download_file(url, dirs)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
    await pablo.edit_text('Uploading...')
    if update.data == 'zip':
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        try:
            await update.message.reply_to_message.reply_document(
                filename,
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except FloodWait as e:
            client.logger.warning(
                'Floodwait for {} seconds'.format(e.value))
            await asyncio.sleep(e.value)
            await update.message.reply_to_message.reply_document(
                filename,
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except Exception:
            client.logger.warning(traceback.format_exc())
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif update.data == '1by1':
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for media in dldirs:
            try:
                await send_media(media, pablo)
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await send_media(media, pablo)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)
