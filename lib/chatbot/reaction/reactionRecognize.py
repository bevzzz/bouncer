from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionRecognize(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)
        self.person = 'Unknown'
        self.error_happened = False

    def response(self):
        if self.error_happened:
            text = "An error occurred while sending a request to Facerec"
        elif self.person == 'Unknown':
            text = f"This person is {self.person}"
        else:
            text = f"I see {self.person}"

        self._send_message(text)

    def action(self):
        file_id, caption = self.message.get_picture_with_caption()
        bytes_picture = self._download_photo(file_id)

        response = self.me.send_request_to_recognize(
            bytes_picture,
            self.user.get_username()
        ).get('response')

        if response['status'] == 200:
            self.person = response['content']['person']
        else:
            self.error_happened = True

    def _download_photo(self, file_id):
        return self.me.chatbot.download_file(file_id)
