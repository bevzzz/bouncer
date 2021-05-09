from lib.chatbot.state.conversationState import ConversationState


class StateRecognize(ConversationState):

    buttons = None

    def __init__(self, context):
        self.photo = None
        super().__init__(context)

    def invoke(self, params):
        self.photo = params.get("photo")

    def act(self):
        pass

    def get_response(self):
        pass
