import abc
import collections

from lib.chatbot.telegramObject import TextMessage, InlineKeyboardButton, InlineKeyboardMarkup


class ConversationState(metaclass=abc.ABCMeta):
    __context = None

    def __init__(self, context):
        self.__context = context

    @abc.abstractmethod
    def invoke(self, params):
        pass

    @abc.abstractmethod
    def act(self):
        pass

    @abc.abstractmethod
    def get_response(self):
        pass

    def build_message(self, text, buttons=None):
        chat_id = self.__context.update.get_chat_id()
        reply_markup = self.add_keyboard(buttons)

        message_out = TextMessage(
            text=text,
            chat_id=chat_id,
            reply_markup=reply_markup
        )
        return message_out.to_dict()

    @staticmethod
    def add_keyboard(buttons):

        if buttons is None:
            return None

        keyboard = collections.defaultdict(list)

        for key_id in buttons:

            key = buttons[key_id]
            row = str(key["row"])

            keyboard[row].append(
                InlineKeyboardButton(
                    text=key["label"],
                    callback_data=key_id
                )
            )

        keyboard = [i[0] for i in sorted(keyboard.items())]
        return InlineKeyboardMarkup(keyboard)
