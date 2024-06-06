import time
import math
import shlex
import asyncio
import os
import re
import random
import traceback
from typing import Tuple
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import Message
from .. import client


CALLBACK_REGEX = re.compile(r'^zip|1by1$')


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
        files = file_name
        pablo = update
        if not '/' in files:
            caption = files
        else:
            caption = files.split('/')[-1]
        progress_args = ('Uploading...', pablo, time.time())
        if files.lower().endswith(('.mkv', '.mp4')):
            metadata = extractMetadata(createParser(files))
            duration = 0
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
            rndmtime = str(random.randint(0, duration))
            await run_cmd(f'ffmpeg -ss {rndmtime} -i "{files}" -vframes 1 thumbnail.jpg')
            await update.reply_video(files, caption=caption, duration=duration, thumb='thumbnail.jpg', progress=progress_for_pyrogram, progress_args=progress_args)
            os.remove('thumbnail.jpg')
        elif files.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                await update.reply_photo(files, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
            except Exception as e:
                print(e)
                await update.reply_document(files, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
        elif files.lower().endswith(('.mp3')):
            try:
                await update.reply_audio(files, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
            except Exception as e:
                print(e)
                await update.reply_document(files, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
        else:
            await update.reply_document(files, caption=caption, progress=progress_for_pyrogram, progress_args=progress_args)
        return True
    else:
        return False


async def download_file(url: str, dl_path: str):
    command = [
        'yt-dlp',
        '-f', 'best',
        '-i',
        '-o',
        dl_path+'/%(title)s.%(ext)s',
        url
    ]
    await run_cmd(command)


# https://github.com/MysteryBots/UnzipBot/blob/master/UnzipBot/functions.py
async def absolute_paths(directory: str):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
