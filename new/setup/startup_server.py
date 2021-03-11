#!/home/dmytro/pycharm/bouncer/bouncerenv/bin/python3

import logging
import teletubby.tools.globals as glob
from new.server.manager import Manager
from new.server.chatbot.telegramBot import TelegramBot
from new.server.storage.localStorage import LocalStorage

# setup logger
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO
)

# setup chatbot
bot_token = glob.config['telegram']['token']
chatbot = TelegramBot(bot_token)

# setup storage
storage = LocalStorage()

# setup manager
manager = Manager(chatbot, storage)
