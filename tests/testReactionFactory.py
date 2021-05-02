import os
import unittest
from lib.utils.startup_manager import manager
from lib.chatbot.updatesHandler import UpdatesHandler
from lib.chatbot.reaction.reactionFactory import ReactionFactory
from lib.chatbot.reaction.reactionDefault import ReactionDefault
from lib.chatbot.reaction.reactionStart import ReactionStart
from lib.chatbot.reaction.reactionAuthorize import ReactionAuthorize
from lib.chatbot.reaction.reactionNotAuthorized import ReactionNotAuthorized
from lib.chatbot.reaction.reactionDownloadPhoto import ReactionDownloadPhoto
from lib.chatbot.reaction.reactionEnd import ReactionEnd
from lib.chatbot.reaction.reactionCommandUnknown import ReactionCommandUnknown
from lib.chatbot.reaction.reactionRecognize import ReactionRecognize
from lib.chatbot.reaction.reactionTrainModel import ReactionTrainModel


class TestReactionFactory(unittest.TestCase):

    @staticmethod
    def get_cb_with(cmd=None):
        cb = {'update_id': 317007529, 'callback_query': {'id': '488459458556047547', 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'message': {'message_id': 17, 'from': {'id': 1790996180, 'is_bot': True, 'first_name': 'Sobaka', 'username': 'dvoretzki_bot'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760482, 'text': 'Hi, Dima!', 'reply_markup': {'inline_keyboard': [[{'text': 'Recognize', 'callback_data': 'recognize'}], [{'text': 'Save photo', 'callback_data': 'save_photo'}], [{'text': 'Train', 'callback_data': 'train'}]]}}, 'chat_instance': '-3889430022395058016', 'data': 'recognize'}}
        if cmd is not None:
            cb['callback_query']['data'] = cmd

        return UpdatesHandler.factory(cb)

    @staticmethod
    def get_msg_with(cmd=None, photo=False):
        msg = {'update_id': 317007528, 'message': {'message_id': 16, 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760481, 'text': 'Test'}}
        if cmd is not None:
            msg = {'update_id': 317007528, 'message': {'message_id': 16, 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760481, 'text': 'Test', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
            msg['message']['text'] = f'/{cmd}'
        if photo:
            msg = {'update_id': 317007528, 'message': {'message_id': 16, 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760481, 'text': 'Test', 'photo': [{'file_id': 'AgACAgIAAxkBAAMaYI6Yd6lz4W1fA4ze_NhnqNWuRA8AAq6zMRtHKXlIUo519LSCRQJw8AGfLgADAQADAgADbQADhcEDAAEfBA', 'file_unique_id': 'AQADcPABny4AA4XBAwAB', 'file_size': 18998, 'width': 240, 'height': 320}, {'file_id': 'AgACAgIAAxkBAAMaYI6Yd6lz4W1fA4ze_NhnqNWuRA8AAq6zMRtHKXlIUo519LSCRQJw8AGfLgADAQADAgADeAADh8EDAAEfBA', 'file_unique_id': 'AQADcPABny4AA4fBAwAB', 'file_size': 80457, 'width': 601, 'height': 800}, {'file_id': 'AgACAgIAAxkBAAMaYI6Yd6lz4W1fA4ze_NhnqNWuRA8AAq6zMRtHKXlIUo519LSCRQJw8AGfLgADAQADAgADeQADiMEDAAEfBA', 'file_unique_id': 'AQADcPABny4AA4jBAwAB', 'file_size': 123157, 'width': 961, 'height': 1280}]}}
        return UpdatesHandler.factory(msg)

    def test_command_start(self):
        # arrange
        message = self.get_cb_with(cmd='start')
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get(), ReactionStart)

    def test_command_end(self):
        # arrange
        message = self.get_cb_with(cmd='end')
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get(), ReactionEnd)

    def test_command_recognize(self):
        # arrange
        message = self.get_cb_with(cmd='recognize')
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get(), ReactionDefault)

    def test_act_recognize_photo(self):
        # arrange
        message = self.get_msg_with(photo=True)
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get('recognize'), ReactionRecognize)

    def test_command_train(self):
        # arrange
        message = self.get_cb_with(cmd='train')
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get(), ReactionTrainModel)

    def test_command_save_photo(self):
        # arrange
        message = self.get_cb_with(cmd='save_photo')
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get(), ReactionDefault)

    def test_act_save_photo(self):
        # arrange
        message = self.get_msg_with(photo=True)
        # act
        rf = ReactionFactory(message, manager)
        # assert
        self.assertIsInstance(rf.get('save_photo'), ReactionDownloadPhoto)


if __name__ == '__main__':
    unittest.main()
