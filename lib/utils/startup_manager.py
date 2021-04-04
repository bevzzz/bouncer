#!/home/dmytro/pycharm/bouncer/bouncerenv/bin/python3

import logging
from lib.manager import Manager
from lib.chatbot.telegramBot import TelegramBot
from lib.storage.localStorage import LocalStorage

# setup logger
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO
)

# setup storage
storage = LocalStorage()

# setup chatbot
storage.set_root_path('')
token_file = storage.read_json('config', 'tokens.json')
chatbot = TelegramBot(token_file['bot_token'])


# setup manager
storage.set_root_path('images')
manager = Manager(chatbot, storage)
