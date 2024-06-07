import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config(object):

    # Your API HASH
    API_HASH = os.environ.get('API_HASH')

    # Your API ID
    APP_ID = int(os.environ.get('APP_ID'))

    # Your Bot Token
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    # Your Telegram ID (optional)
    OWNER_ID = os.environ.get('OWNER_ID')

    # Upload method (default to False)
    AS_ZIP = bool(os.environ.get('AS_ZIP', False))

    PLUGINS = {'root': 'Bot.plugins'}
    
    DOWNLOAD_DIR = "./downloads/"