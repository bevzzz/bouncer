from abc import ABCMeta, abstractmethod
from new.server.chatbot.telegramObject import TextMessage


class ReactionBase(metaclass=ABCMeta):

    def __init__(self, message, me):
        self.message = message
        self.me = me
        self.user = message.get_author()

    def _send_message(self, msg):
        message_out = TextMessage(
            text=msg,
            chat_id=self.message.get_chat_id()
        )
        self.me.chatbot.send_message(message_out.to_dict())

    @abstractmethod
    def response(self):
        pass

    @abstractmethod
    def action(self):
        pass
