from new.server.chatbot.reaction.reactionFactory import ReactionBase


class ReactionStart(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "Hi, {}!".format(self.user.get_name())
        self._send_message(text)

    def action(self):
        pass
