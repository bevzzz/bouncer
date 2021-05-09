import re
from abc import ABCMeta, abstractmethod
from lib.chatbot.telegramObject import TextMessage, InlineKeyboardButton, InlineKeyboardMarkup


class ReactionBase(metaclass=ABCMeta):

    def __init__(self, message, me, options={}):
        self.message = message
        self.me = me
        self.user = message.get_author()

    @abstractmethod
    def response(self):
        pass

    @abstractmethod
    def action(self):
        pass

    def build_message(self, msg, keys=None):

        message_out = TextMessage(
            text=msg,
            chat_id=self.message.get_chat_id(),
            reply_markup=self._build_keyboard(keys)
        )
        return message_out.to_dict()

    def _build_keyboard(self, keys, ncol=1):

        if keys is None:
            return None

        # TODO: arrange buttons in rows
        keyboard = []
        for key in keys:

            keyboard.append(
                # Every keyboard row must be a list of buttons
                [
                    InlineKeyboardButton(
                        text=key,
                        callback_data=self._build_callback_data(key)
                    )
                ]
            )

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def _build_callback_data(key):

        key = re.sub(" ", "_", key)
        return key.lower()

    def _send_message(self, msg, keys=None):

        message_out = TextMessage(
            text=msg,
            chat_id=self.message.get_chat_id(),
            reply_markup=self._build_keyboard(keys)
        )

        self.me.chatbot.send_message(message_out.to_dict())
