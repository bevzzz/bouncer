from lib.chatbot.state.conversationState import ConversationState


class StateMain(ConversationState):

    buttons = {
        "recognize": {
            "label": "Recognize",
            "row": 1,
            "next": "StateAwait"
        },
        "add_photo": {
            "label": "Add photo",
            "row": 1,
            "next": "StateAwait"
        },
        "end": {
            "label": "Exit",
            "row": 2,
            "next": None
        }
    }

    def __init__(self, context):
        super().__init__(context)

    def invoke(self, params):
        pass

    def act(self):
        pass

    def get_response(self):
        name = "User"
        text = f"How can I help you, {name}?"

        # TODO: add Train button if the user has the right permission

        return self.build_message(text=text)

    def set_next_state(self):
        super().set_next_state()
