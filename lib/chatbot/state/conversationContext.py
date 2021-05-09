import logging

from lib.chatbot.state.stateMain import StateMain
from lib.chatbot.state.stateAwait import StateAwait


class ConversationContext:
    __state = None
    __last_state = None

    __state_library = {
        "need_wait": ["recognize", "add_photo"],
        "no_wait": {
            "start": StateMain,
            "train": StateTrain,
        }
    }

    __instances = {}

    def __init__(self, parent, update):
        self.parent = parent
        self.update = update

        self.log = logging.getLogger()
        self.__instances[update.get_chat_id()] = self

    @classmethod
    def open(cls, parent, update):
        chat_id = update.get_chat_id()

        if chat_id in cls.__instances:
            return cls.__instances[chat_id]
        else:
            return ConversationContext(parent, update)

    def reply(self):
        self.__last_state = self.__state

        if self.__state is None:
            state = self._factory(
                msg=self.update.get_phrase()
            )
            self._change_state(state)

        params = {
            # TODO: pass params elegantly
        }

        self.__state.invoke(params)
        self.__state.act()
        response = self.__state.get_respose()

        self.parent._update_message(
            to_delete=self.update,
            to_send=response
        )

    def _change_state(self, state):
        self.__state = state

    def _factory(self, msg=None):
        if msg == 'back':
            return self.__last_state

        if msg in self.__state_library["need_wait"]:
            state = StateAwait
        else:
            state = self.__state_library["no_wait"].get(msg, StateUnknownInput)

        return state(self)