from lib.chatbot.state.conversationState import ConversationState


class StateAddPhoto(ConversationState):

    buttons = {
        "add_photo": {
            "label": "Try again",
            "row": 1,
            "next": "StateAwait"
        },
        "main": {
            "label": "Back to main",
            "row": 2,
            "next": "StateMain"
        }
    }

    def __init__(self, context):
        self.photo = None
        self.error_happened = False
        super().__init__(context)

    def invoke(self, params):
        self.photo = self.download_photo()

    def act(self):
        try:
            self.store_photo(self.photo)
        except AttributeError as err:
            self.log.warning(err)
            self.error_happened = True

    def get_response(self):
        if not self.error_happened:
            text = "Nice pic! I added it to your personal folder"
        else:
            text = "Oh crap, I couldn't download that. Try again with a different photo"

        return self.build_message(text=text)

    def set_next_state(self):
        super().set_next_state()
