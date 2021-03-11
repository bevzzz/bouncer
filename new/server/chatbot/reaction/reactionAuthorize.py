from new.server.chatbot.reaction.reactionBase import ReactionBase


class ReactionAuthorize(ReactionBase):

    def __init__(self, message, me, state):
        super().__init__(message, me)
        self.state = state

    def response(self):

        if self.state == 'await_password':
            text = 'Please type in your password'
        else:
            if self._is_correct_password():
                text = "Congratulations, you're logged in"

    def action(self):
        pass

    def _is_correct_password(self):
        pass
