import logging, sys, time, os
from pathlib import Path
from os import environ as env

from ruamel.yaml import YAML

import telegram.ext
from pyrogram import Client

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# Config
TELEGRAM_BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN")

config_file = Path(os.path.join(__name__, "config.yaml"))
yaml = YAML(typ="safe")
config_data = yaml.load(config_file)  # look for ./crawl/config.yaml

OWNER_USERID = int(config_data.get("OWNER_USERID"))
OWNER_USERNAME = config_data.get("OWNER_USERNAME")
PREFIX = config_data.get("PREFIX")
JOIN_LOGGER = config_data.get("JOIN_LOGGER")
ALLOW_CHATS = config_data.get("ALLOW_CHATS")
DEV_USERS = frozenset((config_data.get("DEV_USERS") or []) + [OWNER_USERID])
SUPPORT_USERS = set((config_data.get("SUPPORT_USERS") or []) + [OWNER_USERID])
EVENT_LOGS = config_data.get("EVENT_LOGS")
WEBHOOK = config_data.get("WEBHOOK")
URL = config_data.get("URL")
PORT = config_data.get("PORT")
CERT_PATH = config_data.get("CERT_PATH")
API_ID = config_data.get("API_ID")
API_HASH = config_data.get("API_HASH")

DB_URI = config_data.get("SQLALCHEMY_DATABASE_URI")
DONATION_LINK = config_data.get("DONATION_LINK")
LOAD = config_data.get("LOAD")
NO_LOAD = config_data.get("NO_LOAD")
DEL_CMDS = config_data.get("DEL_CMDS")
CASH_API_KEY = config_data.get("CASH_API_KEY")
TIME_API_KEY = config_data.get("TIME_API_KEY")
WALL_API = config_data.get("WALL_API")
SUPPORT_CHAT = config_data.get("SUPPORT_CHAT")
BL_CHATS = frozenset(config_data.get("BL_CHATS") or [])

updater = telegram.ext.Updater(TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher

pyrogram_app = Client(
    "clara",
    env.get("TELEGRAM_API_ID"),
    env.get("TELEGRAM_API_HASH"),
    bot_token=env.get("TELEGRAM_BOT_TOKEN"),
)

# Load at end to ensure all prev variables have been set
from SaitamaRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
telegram.ext.RegexHandler = CustomRegexHandler
telegram.ext.CommandHandler = CustomCommandHandler
telegram.ext.MessageHandler = CustomMessageHandler
