import logging

from lib.chatbot.state.stateMain import StateMain
from lib.chatbot.state.stateAwait import StateAwait
from lib.chatbot.state.stateTrain import StateTrain
from lib.chatbot.state.stateUnknownInput import StateUnknownInput


class ConversationContext:

    _state_library = {
        "need_wait": ["recognize", "add_photo"],
        "no_wait": {
            "start": StateMain,
            "train": StateTrain,
        }
    }

    _instances = {}

    def __init__(self, parent, update):
        self.log = logging.getLogger()

        self.parent = parent
        self.update = update

        self._last_message_id = None
        self.last_state = None
        self._state = None
        self._instances[update.get_chat_id()] = self

    @classmethod
    def open(cls, parent, update):
        chat_id = update.get_chat_id()
        if chat_id in cls._instances:
            instance = cls._instances[chat_id]
            instance.set_update(update)
            return instance
        else:
            return ConversationContext(parent, update)

    def set_update(self, update):
        self.update = update

    def reply(self):
        # set default state
        if self._state is None:
            self.change_state(StateMain(self))

        # pass necessary parameters
        params = {
            # TODO: pass params elegantly
        }
        self._state.invoke(params)

        # handle states
        if self.update.get_phrase() != 'start':
            last_state = self._state
            self._state.set_next_state()
            self.last_state = last_state

        # execute command
        self._state.act()

        # update ui
        response = self._state.get_response()
        msg_id = self.parent.update_message(
            chat_id=self.update.get_chat_id(),
            to_delete_id=self._last_message_id,
            to_send=response
        )
        self._last_message_id = msg_id

    def change_state(self, state):
        self._state = state

    def _factory(self, msg=None):
        if msg == 'back':
            return self.last_state

        if msg in self._state_library["need_wait"]:
            state = StateAwait
        else:
            state = self._state_library["no_wait"].get(msg, StateUnknownInput)

        return state
