from new.server.chatbot.reaction.reactionFactory import ReactionFactory
from new.server.chatbot.conversation import Conversation
import logging
import time


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

    def is_authorized_user(self, user):
        user_roles = self.storage.read_config_json('users.json')
        return user.get_username() in list(user_roles.keys())


