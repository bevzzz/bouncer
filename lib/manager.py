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

    def get_user_roles(self):
        self.storage.set_root_path('')
        user_roles = self.storage.read_json('config', 'users.json')
        self.storage.set_root_path('images')

        return user_roles

    def is_authorized_user(self, user):
        user_roles = self.get_user_roles()
        return user.get_username() in list(user_roles.keys())

    def is_admin(self, user):
        user_roles = self.get_user_roles()
        return user_roles[user.get_username()] == 'admin'

    @staticmethod
    def send_request_to_recognize(img):
        base_url = 'http://localhost:5000/bouncer/v1/model/recognize'
        img = base64.encodebytes(img).decode('utf-8')

        body_json = {
            'img': img
        }

        response = requests.post(url=base_url, json=body_json)
        return response.json()

    def send_request_to_train(self, people=None):
        base_url = 'http://localhost:5000/bouncer/v1/model/train'

        if people is None:
            people = self.get_user_roles()
            people = list(people.keys())

        body_json = {
            'people': people
        }

        response = requests.post(url=base_url, json=body_json)
        return response.json()

