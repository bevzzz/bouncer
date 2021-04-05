from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionNotAuthorized(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "Thanks, but I'm not supposed to be downloading your pictures :("
        self._send_message(text)

    def action(self):
        super().action()
