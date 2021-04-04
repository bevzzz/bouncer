from lib.chatbot.reaction.reactionFactory import ReactionFactory
from lib.chatbot.conversation import Conversation
import logging
import time
import base64
import requests


class Manager:

    def __init__(self, chatbot, storage):
        self.chatbot = chatbot
        self.storage = storage
        self.conversations = []
        self.log = logging.getLogger()

    def talk(self):
        self.log.info("start talk()")

        while True:

            conversations = self._update_conversations()
            for conv in conversations:
                for msg in conv.get_new_messages():
                    self._react_to_message(msg)

            self.chatbot.update_offset()

            time.sleep(1)

    def _update_conversations(self):
        updates = self.chatbot.get_updates()
        conversations = Conversation.open_conversations(updates)

        for conv in conversations:
            self.conversations.append(conv)

        return conversations

    def _react_to_message(self, message):
        reaction = ReactionFactory(message, self).get()
        reaction.action()
        reaction.response()
        message.mark_as_read()

    def _get_user_roles(self):
        self.storage.set_root_path('')
        user_roles = self.storage.read_json('config', 'users.json')
        self.storage.set_root_path('images')

        return user_roles

    def is_authorized_user(self, user):
        user_roles = self._get_user_roles()
        return user.get_username() in list(user_roles.keys())

    @staticmethod
    def send_request_to_recognize(self, img):
        base_url = 'http://localhost:5000/bouncer/v1/model/recognize'
        img = base64.encodebytes(img).decode('utf-8')
        data = {
            'img': img
        }

        response = requests.post(url=base_url, data=data)

        return response.json

    @staticmethod
    def send_request_to_train(self, people=None):
        base_url = 'http://localhost:5000/bouncer/v1/model/train'

        if people is None:
            people = self._get_user_roles()
            people = list(people.keys())

        data = {
            'people': people
        }

        response = requests.post(url=base_url, data=data)

        return response.json

