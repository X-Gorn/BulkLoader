## BulkLoader (Bot)

---

Telegram Bot to Bulk Downloading list of urls and Upload to Telegram.

### Features:

#### Upload list of urls (2 methods):

- send command `/link` and then send urls, separated by new line.
- send txt file (links), separated by new line.

## Deploying

### Docker

Install Docker

`/bin/bash -c "$(curl -fsSL https://git.io/JDGfm)"`

Refresh User State

`sudo su -l $USER`

Running Docker Server

`docker run -d -e API_HASH=abc -e APP_ID=123 -e BOT_TOKEN="123:abc" -e OWNER_ID=12345678 -e AS_ZIP=false -e BUTTONS=true xgorn/bulkloader:latest`

## Telegram Support:

[![Group](https://img.shields.io/badge/TG-Group-30302f?style=flat&logo=telegram)](https://t.me/WeebProgrammer)

## Credits, and Thanks to

- [Dan Tès](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)

#### LICENSE

- GPLv3
