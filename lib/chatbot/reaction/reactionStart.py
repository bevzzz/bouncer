from lib.chatbot.reaction.reactionBase import ReactionBase


class ReactionStart(ReactionBase):

    def __init__(self, message, me, options={}):
        super().__init__(message, me, options)

    def take_action(self):
        pass

    def get_response(self):
        text = "Hi, {}!".format(self.user.get_name())
        keys = [
            "Recognize",
            "Save photo"
        ]

        if self.me.is_authorized_user(self.user):
            keys.append("Train")

        return self.build_message(text, keys)

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
