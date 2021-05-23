from lib.chatbot.state.conversationState import ConversationState

from lib.chatbot.state.stateRecognize import StateRecognize
from lib.chatbot.state.stateAddPhoto import StateAddPhoto


class StateAwait(ConversationState):

    buttons = {
        "back": {
            "label": "Back",
            "row": 1,
            "next": 'last_state'
        }
    }

    def __init__(self, context):
        self.msg = None
        super().__init__(context)

    def invoke(self, params):
        self.msg = self._context.update.get_phrase()

    def act(self):
        pass

    def get_response(self):
        return self.build_message(text="waiting...")

    def set_next_state(self):
        if self._context.update.get_phrase() in self.buttons:
            super().set_next_state()
        else:
            self._set_next_state()

    def _set_next_state(self):
        if self.msg == "recognize":
            state = StateRecognize(self._context)
        elif self.msg == "add_photo":
            state = StateAddPhoto(self._context)
        else:
            state = self

        self._context.change_state(state)


