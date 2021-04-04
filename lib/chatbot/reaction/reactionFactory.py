import re
from lib.chatbot.reaction.reactionDefault import ReactionDefault
from lib.chatbot.reaction.reactionStart import ReactionStart
from lib.chatbot.reaction.reactionAuthorize import ReactionAuthorize
from lib.chatbot.reaction.reactionNotAuthorized import ReactionNotAuthorized
from lib.chatbot.reaction.reactionDownloadPhoto import ReactionDownloadPhoto
from lib.chatbot.reaction.reactionEnd import ReactionEnd
from lib.chatbot.reaction.reactionCommandUnknown import ReactionCommandUnknown


class ReactionFactory:

    def __init__(self, message, me):
        self.message = message
        self.me = me

    @staticmethod
    def _is_command(msg):
        return re.match('/', msg)

    def get(self):
        msg = self.message.get_text()
        user = self.message.get_author()

        params = {
            'message': self.message,
            'me': self.me
        }

        if self._is_command(msg):

            if msg == '/start':
                reaction = ReactionStart
            elif msg == '/authorize':
                reaction = ReactionCommandUnknown
            elif msg == '/end':
                reaction = ReactionEnd
            else:
                reaction = ReactionCommandUnknown

        elif self.message.has_photo():

            if self.me.is_authorized_user(user):
                reaction = ReactionDownloadPhoto
            else:
                reaction = ReactionNotAuthorized

        else:
            reaction = ReactionDefault

        return reaction(**params)
