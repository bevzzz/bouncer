import collections
from new.server.chatbot.updatesHandler import UpdatesHandler


class Conversation:
    """
    Keeps track of all the conversations (i.e. chats) in which a bot is present.
    Has methods to record incoming messages and react to them. Receives a raw message
    from TelegramBot, passes it to MessageDTO and receives the text body or
    notification about a file etc. Understands bot commands a.k.a. /start and alike (?)
    """

    instances = {}

    def __init__(self, message_dto):
        self.chat_id = message_dto.get_chat_id()
        self.is_private = message_dto.is_private_chat()
        self.instances[self.chat_id] = self
        self.messages = {}
        self.members = []

    @staticmethod
    def open_conversations(updates):
        active_conv = collections.defaultdict()

        for upd in updates:
            msg = UpdatesHandler.factory(upd)
            this_conv = Conversation._get_instance(msg)
            active_conv[msg.get_chat_id()] = this_conv
            this_conv._add_new_message(msg)

        return list(active_conv.values())

    @classmethod
    def _get_instance(cls, message_dto):
        try:
            chat_id = message_dto.get_chat_id()
            conversation = cls.instances[chat_id]
        except KeyError:
            conversation = cls(message_dto)
        return conversation

    def _add_new_messages(self, messages):
        for msg in messages:
            self._add_new_message(msg)

    def _add_new_message(self, msg):
        self.messages[msg.get_message_id()] = msg

    def get_new_messages(self):
        new_messages = [msg for msg in self.messages.values() if not msg.is_read()]
        return new_messages
