from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionTrainModel(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)
        self.error_happened = False
        self.message_contents = None

    def take_action(self):
        self.action()

    def get_response(self):
        if self.error_happened:
            text = "An error occurred while sending a request to FacerecTrain"
        else:
            text = f"{self.message_contents['message']}. " \
                   f"The training set has {self.message_contents['image_count']} pictures"

        return self.build_message(text)

    def response(self):
        if self.error_happened:
            text = "An error occurred while sending a request to FacerecTrain"
        else:
            text = f"{self.message_contents['message']}. " \
                   f"The training set has {self.message_contents['image_count']} pictures"

        self._send_message(text)

    def action(self):
        users = self.me.get_user_roles()

        response = self.me.send_request_to_train(
            list(users.keys())
        ).get('response')

        self.me.log.info(response)

        if response['status'] == 200:
            self.message_contents = response['content']
        else:
            self.error_happened = True
