import time
import math
import shlex
import asyncio
import os
import re
import random
import traceback
from typing import Tuple
from pyrogram.errors import FloodWait
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import Message
from ..config import Config
from .. import client


FFMPEG_REGEX = re.compile(
    pattern=r'(?:ftp|amqp|rtmp|mmsh|mmst|icecast|rtmpe|rtmps|rtmpt|rtmpte|rtmpts|smb|sftp|rtp|rtsp|sap|sctp|srt|srtp|tcp|tls|udp|unix|zmq)://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

# Detect URLS using Regex. https://stackoverflow.com/a/3809435/15561455
URL_REGEX = re.compile(
    pattern=r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')


# https://github.com/SpEcHiDe/AnyDLBot
async def progress_for_pyrogram(
    current: float,
    total: float,
    ud_type: str,
    message: Message,
    start: float
) -> None:
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except Exception:
            client.logger.warning(traceback.format_exc())


def humanbytes(size: int) -> str:
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


async def run_cmd(cmd) -> Tuple[str, str, int, int]:
    if type(cmd) == str:
        cmd = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


# Send media; ffmpeg required
async def send_media(file_name: str, update: Message) -> bool:
    if os.path.isfile(file_name):
        caption = client.custom_caption.get(update.chat.id, '')
        if not caption:
            if not '/' in file_name:
                caption = file_name
            else:
                caption = file_name.split('/')[-1]
        progress_args = ('Uploading...', update, time.time())
        thumbnail = client.custom_thumbnail.get(update.chat.id)
        if file_name.lower().endswith(('.mkv', '.mp4')):
            metadata = extractMetadata(createParser(file_name))
            duration = 0
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
            rndmtime = str(random.randint(0, duration))
            if not thumbnail:
                thumbnail = file_name+'.jpg'
                await run_cmd(f'ffmpeg -ss {rndmtime} -i "{file_name}" -vframes 1 "{thumbnail}"')
            sended_media = await update.reply_video(file_name, caption=caption, duration=duration, thumb=thumbnail, progress=progress_for_pyrogram, progress_args=progress_args)
        elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                sended_media = await update.reply_photo(file_name, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
            except Exception:
                client.logger.warning(traceback.format_exc())
                sended_media = await update.reply_document(file_name, caption=caption, thumb=thumbnail, progress=progress_for_pyrogram, progress_args=progress_args)
        elif file_name.lower().endswith(('.mp3')):
            duration = 0
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
            try:
                sended_media = await update.reply_audio(file_name, caption=caption, duration=duration, thumb=thumbnail, progress=progress_for_pyrogram, progress_args=progress_args)
            except Exception as e:
                client.logger.warning(traceback.format_exc())
                sended_media = await update.reply_document(file_name, caption=caption, thumb=thumbnail, progress=progress_for_pyrogram, progress_args=progress_args)
        else:
            sended_media = await update.reply_document(file_name, caption=caption, thumb=thumbnail, progress=progress_for_pyrogram, progress_args=progress_args)
        if Config.DUMP_ID:
            try:
                await sended_media.forward(Config.DUMP_ID)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await sended_media.forward(Config.DUMP_ID)
            except Exception:
                client.logger.warning(traceback.format_exc())
        return True
    else:
        return False


async def download_file(url: str, dl_path: str):
    command = 'yt-dlp -vU -f best -i -o "{}/%(title)s.%(ext)s" "{}"'.format(
        dl_path, url
    )
    await run_cmd(command)


async def stream_ffmpeg(url: str, dl_path: str):
    command = 'ffmpeg -i "{}" -c copy "{}"'.format(
        url, dl_path,
    )
    await run_cmd(command)


# https://github.com/MysteryBots/UnzipBot/blob/master/UnzipBot/functions.py
async def absolute_paths(directory: str):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
