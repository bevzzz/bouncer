import abc
import collections
import logging
# message elements
from lib.chatbot.telegramObject import TextMessage, InlineKeyboardButton, InlineKeyboardMarkup
# states


class ConversationState(metaclass=abc.ABCMeta):

    buttons = None

    def __init__(self, context):
        self.log = logging.getLogger()
        if context is None:
            self.log.error(f"No context provided for {self}")
            raise RuntimeError
        else:
            self._context = context

    @abc.abstractmethod
    def invoke(self, params):
        pass

    @abc.abstractmethod
    def act(self):
        pass

    @abc.abstractmethod
    def get_response(self):
        pass

    @abc.abstractmethod
    def set_next_state(self):
        msg = self._context.update.get_phrase()
        n = self.buttons[msg]['next']

        if n is None:
            state = self
        elif n == 'last_state':
            state = self._context.last_state
        else:
            # add error handling
            state = self._context.states.get(n, self._context.last_state)
            state = state(self._context)

        self._context.change_state(state)

    def build_message(self, text):
        chat_id = self._context.update.get_chat_id()
        reply_markup = self.add_keyboard(self.buttons)

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

        keyboard = [i[1] for i in sorted(keyboard.items())]
        return InlineKeyboardMarkup(keyboard)
