from new.server.chatbot.reaction.reactionBase import ReactionBase


class ReactionCommandUnknown(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "I don't know this command"
        self._send_message(text)

    def action(self):
        super().action()
