## BulkLoader (Bot)

---

Telegram Bot to Bulk Downloading list of yt-dlp supported urls and Upload to Telegram.

### Features:

#### Upload list of urls (2 methods):

- send command `/link` and then send urls, separated by new line.
- send txt file (links), separated by new line.

<details>
<summary>
    <b style="font-size: 27px"> Environments </b>
</summary>
<br>

`API_HASH`: Get this from my.telegram.org

`APP_ID`: Get this from my.telegram.org

`BOT_TOKEN`: Get this from @BotFather on Telegram.

`AS_ZIP`: Set this to `true` if you want the bot to upload the files as zipfile. Default to `false`

`BUTTONS`: Set this to `true` if you want the bot to ignore `AS_ZIP` and send a button instead.

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

Running Docker Server

`docker run -d -e API_HASH=abc -e APP_ID=123 -e BOT_TOKEN="123:abc" -e OWNER_ID=12345678 -e AS_ZIP=false -e BUTTONS=true xgorn/bulkloader:latest`

</details>

## Telegram Support:

[![Group](https://img.shields.io/badge/TG-Group-30302f?style=flat&logo=telegram)](https://t.me/WeebProgrammer)

## Credits, and Thanks to

- [Dan Tès](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)

#### LICENSE

- GPLv3
