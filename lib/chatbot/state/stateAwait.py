from lib.chatbot.state.conversationState import ConversationState


class StateAwait(ConversationState):

    buttons = {
        "back": {
            "label": "Back",
            "row": 1
        }
    }

    def __init__(self, context):
        self.msg = None
        super().__init__(context)

    def invoke(self, params):
        self.msg = params.get("msg")

    def act(self):

        if self.msg == "recognize":
            state = StateRecognize(self.__context)
        elif self.msg == "add_photo":
            state = StateAddPhoto(self.__context)
        else:
            state = None

        self.__context.changeState(state)

    def get_response(self):

        return self.build_message(
            text="waiting...",
            buttons=self.buttons
        )
