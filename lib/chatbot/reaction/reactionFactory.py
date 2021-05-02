import re
from lib.chatbot.conversation import Conversation
from lib.chatbot.reaction.reactionDefault import ReactionDefault
from lib.chatbot.reaction.reactionStart import ReactionStart
from lib.chatbot.reaction.reactionAuthorize import ReactionAuthorize
from lib.chatbot.reaction.reactionNotAuthorized import ReactionNotAuthorized
from lib.chatbot.reaction.reactionDownloadPhoto import ReactionDownloadPhoto
from lib.chatbot.reaction.reactionEnd import ReactionEnd
from lib.chatbot.reaction.reactionCommandUnknown import ReactionCommandUnknown
from lib.chatbot.reaction.reactionRecognize import ReactionRecognize
from lib.chatbot.reaction.reactionTrainModel import ReactionTrainModel


class ReactionFactory:

    def __init__(self, message, me):
        self.message = message
        self.me = me

    # @staticmethod
    # def _is_command(msg):
    #     return re.match('/', msg)

    def get(self, previous_message=''):
        msg = self.message.get_phrase()
        if not previous_message:
            previous_message = Conversation.get_previous_message(self.message).get_phrase()
        user = self.message.get_author()

        if previous_message == 'recognize':
            print('previous_message')
            print(previous_message)
            print('self.message.has_photo()')
            print(self.message.has_photo())
            print('self.message.is_command()')
            print(self.message.is_command())

        params = {
            'message': self.message,
            'me': self.me
        }

        if self.message.is_command():

            if msg == 'start':
                reaction = ReactionStart
            elif msg in ['recognize', 'save_photo']:
                reaction = ReactionDefault
            elif msg == 'train':
                reaction = ReactionTrainModel
            elif msg == 'end':
                reaction = ReactionEnd
            else:
                reaction = ReactionCommandUnknown

        elif self.message.has_photo():

            if self.me.is_authorized_user(user):
                if previous_message == 'recognize':
                    reaction = ReactionRecognize
                elif previous_message == 'save_photo':
                    reaction = ReactionDownloadPhoto
                else:
                    reaction = ReactionDefault
            else:
                reaction = ReactionNotAuthorized
        else:
            reaction = ReactionDefault

        return reaction(**params)
