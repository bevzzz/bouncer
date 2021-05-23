import logging

from lib.chatbot.state.stateMain import StateMain
from lib.chatbot.state.stateAwait import StateAwait
from lib.chatbot.state.stateRecognize import StateRecognize
from lib.chatbot.state.stateAddPhoto import StateAddPhoto


class ConversationContext:

    states = {
        "StateMain": StateMain,
        "StateAwait": StateAwait,
        "StateRecognize": StateRecognize,
        "StateAddPhoto": StateAddPhoto,
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

        # handle states
        if self.update.get_phrase() != 'start':
            last_state = self._state
            self._state.set_next_state()
            self.last_state = last_state

        # pass necessary parameters
        params = {}
        self._state.invoke(params)
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

    def download_photo(self):
        file_id, caption = self.update.get_picture_with_caption()
        photo = self.parent.chatbot.download_file(file_id)
        return photo

    def store_photo(self, photo, name, to_dir):
        self.parent.storage.write_image(
            img=photo,
            name=name,
            to_dir=to_dir
        )
