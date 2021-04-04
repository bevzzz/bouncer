from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionDefault(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "Uff, I'm speechless..."
        self._send_message(text)

    def action(self):
        pass
