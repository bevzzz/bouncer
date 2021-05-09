from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionEnd(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def take_action(self):
        self.action()

    def get_response(self):
        return self.build_message(msg="Bye!")

    def response(self):
        text = "Bye!"
        self._send_message(text)

    def action(self):
        pass
