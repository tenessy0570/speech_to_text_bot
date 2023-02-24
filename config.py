from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("bot_token")
DB_PATH = Path(__file__).parent / "database" / "db.sqlite3"

SAVE_VOICE_MESSAGE_PATH = Path(__file__).parent / "voice_files_cache"
UNCONVERTED_MESSAGES_PATH = SAVE_VOICE_MESSAGE_PATH / "unconverted_files"
CONVERTED_MESSAGES_PATH = SAVE_VOICE_MESSAGE_PATH / "converted_files"

DEFAULT_UNCONVERTED_FILENAME = "unconverted"
DEFAULT_CONVERTED_FILENAME = "converted"
