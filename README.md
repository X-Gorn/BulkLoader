## BulkLoader (Bot)

---

Telegram Bot to Bulk Downloading list of yt-dlp/ffmpeg supported urls and Upload to Telegram.

### Features:

#### Settings

- `/thumbnail`: custom thumbnail. ex: reply to a photo or do `/thumbnail https...jpg`
- `/caption`: custom thumbnail. ex: `/caption abc`

Note: To clear thumbnail or the caption. do the command without args. ex: `/thumbnail` or `/caption`

#### Upload list of urls (2 methods):

- send links.
- send txt file with links inside it.

#### Link search method:

- regex link search.

Note: Make sure that each link is separated.

### Supported Links

#### FFMPEG

ftp, amqp, rtmp, mmsh, mmst, icecast, rtmpe, rtmps, rtmpt, rtmpte, rtmpts, smb, sftp, rtp, rtsp, sap, sctp, srt, srtp, tcp, tls, udp, unix, zmq.

https://www.ffmpeg.org/ffmpeg-protocols.html

#### YT-DLP

https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

<details>
<summary>
    <b style="font-size: 27px"> Environments </b>
</summary>
<br>

`API_HASH`: Get this from my.telegram.org

`APP_ID`: Get this from my.telegram.org

`BOT_TOKEN`: Get this from @BotFather on Telegram.

`OWNER_ID`: Your Telegram ID.

`DUMP_ID`: Your Telegram Channel/Group ID to Dump the Uploaded Files. let it empty if you don't need it.

`AS_ZIP`: Set this to `True` if you want the bot to zip downloaded files before uploading. Default to `False`

</details>

## Deployments:

<details>
<summary>
    <b> Docker </b>
</summary>
<br>

Install Docker

`/bin/bash -c "$(curl -fsSL https://git.io/JDGfm)"`

Refresh User State

`sudo su -l $USER`

Run Docker Container

`docker run --name=bulkloader -d -e API_HASH=abc -e APP_ID=123 -e BOT_TOKEN="123:abc" -e OWNER_ID=12345678 -e AS_ZIP=False xgorn/bulkloader:latest`

Restart Docker Container

`docker restart bulkloader`

Stop and Remove Docker Container (useful when you want to update the image to the latest and run it again)

```
docker stop bulkloader
docker rm bulkloader
```

Update Image to Latest

`docker pull xgorn/bulkloader:latest`

Redeploy Docker Container with Latest Image(one command)

`docker stop bulkloader && docker rm bulkloader && docker pull xgorn/bulkloader:latest && docker run --name=bulkloader -d -e API_HASH=abc -e APP_ID=123 -e BOT_TOKEN="123:abc" -e OWNER_ID=12345678 -e AS_ZIP=False xgorn/bulkloader:latest`

</details>

<details>
<summary>
    <b> Heroku </b>
</summary>
<br>

<a href="https://www.heroku.com/deploy"><img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy"></a>

</details>

## Telegram Support:

[![Group](https://img.shields.io/badge/TG-Group-30302f?style=flat&logo=telegram)](https://t.me/WeebProgrammer)

## Credits, and Thanks to

- [Dan Tès](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)

#### LICENSE

- GPLv3
