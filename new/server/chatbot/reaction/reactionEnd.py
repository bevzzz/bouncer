from new.server.chatbot.reaction.reactionBase import ReactionBase


class ReactionEnd(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "Bye!"
        self._send_message(text)

    def action(self):
        super().action()
