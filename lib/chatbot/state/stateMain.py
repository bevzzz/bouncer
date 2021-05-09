from lib.chatbot.state.conversationState import ConversationState


class StateMain(ConversationState):

    buttons = {
        "recognize": {
            "label": "Recognize",
            "row": 1
        },
        "add_photo": {
            "label": "Add photo",
            "row": 1
        },
        "end": {
            "label": "Exit",
            "row": 2
        }
    }

    def invoke(self, params):
        pass

    def act(self):
        pass

    def get_response(self):
        name = "User"
        text = f"How can I help you, {name}?"

        # TODO: add Train button if the user has the right permission

        return self.build_message(
            text=text,
            buttons=self.buttons
        )

