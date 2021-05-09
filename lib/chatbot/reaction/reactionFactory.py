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

    reactions = {
        'start': ReactionStart,
        'save_photo': ReactionDownloadPhoto,
        'recognize': ReactionRecognize,
        'train': ReactionTrainModel,
        'end': ReactionEnd
    }

    def __init__(self, parent):
        self.parent = parent

    def get(self, message=None, photo=None, state=None):
        msg = message.get_phrase()
        user = message.get_author()

        params = {
            'message': message,
            'me': self.parent
        }

        if message.is_command():

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

        elif message.has_photo():

            if self.parent.is_authorized_user(user):
                if state == 'recognize':
                    reaction = ReactionRecognize
                elif state == 'save_photo':
                    reaction = ReactionDownloadPhoto
                else:
                    reaction = ReactionDefault
            else:
                reaction = ReactionNotAuthorized
        else:
            reaction = ReactionDefault

        return reaction(**params)

    def _get(self, message=None, photo=None, state=None):

        text = message.get_phrase()
        params = {
            'message': message,
            'me': self.parent,
            'options': None
        }

        if text in self.reactions:
            reaction = self.reactions[text]

            if photo is not None:
                params['options']['photo'] = photo

            if state is not None:
                params['options']['state'] = state

        else:
            reaction = ReactionDefault

        return reaction(**params)