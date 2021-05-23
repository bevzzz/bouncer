from lib.chatbot.state.conversationState import ConversationState


class StateRecognize(ConversationState):

    buttons = {
        "main": {
            "label": "Back to main",
            "row": 1,
            "next": "StateMain"
        }
    }

    def __init__(self, context):
        self.photo = None
        self.people_in_photo = None
        self.error_happened = None
        super().__init__(context)

    def invoke(self, params):
        self.photo = self.download_photo()

    def act(self):
        response = self._context.parent.send_request_to_recognize(
            self.photo
        ).get('response')

        if response['status'] == 200:
            self.people_in_photo = response['content']['person']
        else:
            self.error_happened = True

    def get_response(self):
        if self.error_happened:
            text = "Sorry, an error occurred while sending a request to Facerec"
        elif not len(self.people_in_photo):
            text = "Couldn't find a face in this photo :("
        elif self._unknown_person():
            text = "I do not know this person"
        else:
            text = f"I see {', '.join(self.people_in_photo)}"

        return self.build_message(text=text)

    def _unknown_person(self):
        return self.people_in_photo[0] == 'Unknown'

    def set_next_state(self):
        super().set_next_state()
