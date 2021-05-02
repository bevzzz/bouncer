from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionStart(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)

    def response(self):
        text = "Hi, {}!".format(self.user.get_name())

        keys = [
            "Recognize",
            "Save photo"
        ]

        if self.me.is_authorized_user(self.user):
            keys.append("Train")

        self._send_message(text, keys)

    def action(self):
        pass
