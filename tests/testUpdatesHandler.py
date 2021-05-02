import unittest
from lib.chatbot.updatesHandler import UpdatesHandler
from lib.chatbot.updatesHandler import MessageDTO
from lib.chatbot.updatesHandler import CallbackDTO
from lib.utils.user import Owner


class UpdatesHandlerTest(unittest.TestCase):

    valid_message = {'update_id': 317007528, 'message': {'message_id': 16, 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760481, 'text': '/recognize', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
    valid_callback = {'update_id': 317007529, 'callback_query': {'id': '488459458556047547', 'from': {'id': 113728330, 'is_bot': False, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'language_code': 'en'}, 'message': {'message_id': 17, 'from': {'id': 1790996180, 'is_bot': True, 'first_name': 'Sobaka', 'username': 'dvoretzki_bot'}, 'chat': {'id': 113728330, 'first_name': 'Dima', 'last_name': 'Solovei', 'username': 'bevzzz', 'type': 'private'}, 'date': 1619760482, 'text': 'Hi, Dima!', 'reply_markup': {'inline_keyboard': [[{'text': 'Recognize', 'callback_data': 'recognize'}], [{'text': 'Save photo', 'callback_data': 'save_photo'}], [{'text': 'Train', 'callback_data': 'train'}]]}}, 'chat_instance': '-3889430022395058016', 'data': 'recognize'}}

    def get_MessageDTO(self):
        message = self.valid_message.get('message')
        return MessageDTO(message)

    def get_CallbackDTO(self):
        cb = self.valid_callback.get('callback_query')
        return CallbackDTO(cb)

    def test_factory_msg(self):
        # arrange
        # act
        handler = UpdatesHandler().factory(self.valid_message)
        # assert
        self.assertIsInstance(handler, MessageDTO)

    def test_factory_cb(self):
        # arrange
        # act
        handler = UpdatesHandler().factory(self.valid_callback)
        # assert
        self.assertIsInstance(handler, CallbackDTO)

    def test_create_message_dto(self):
        # arrange
        message = self.valid_message.get('message')
        # act
        handler = MessageDTO(message)
        # assert
        self.assertIsNotNone(handler)
        self.assertFalse(handler.is_read())
        self.assertIsInstance(handler.get_author(), Owner)

    def test_create_callback_dto(self):
        # arrange
        cb = self.valid_callback.get('callback_query')
        # act
        handler = CallbackDTO(cb)
        # assert
        self.assertFalse(handler.has_photo())
        self.assertIsInstance(handler.get_author(), Owner)

    def test_mark_as_read_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        handler.mark_as_read()
        # assert
        self.assertTrue(handler.is_read())

    def test_get_chat_id_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        chat_id = handler.get_chat_id()
        # assert
        self.assertEqual(chat_id, '113728330')

    def test_get_message_id(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        message_id = handler.get_message_id()
        # assert
        self.assertEqual(message_id, 16)

    def test_is_private_cb(self):
        # arrange
        handler = self.get_CallbackDTO()
        # act
        # assert
        self.assertTrue(handler.is_private_chat())

    def test_is_private_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        # assert
        self.assertTrue(handler.is_private_chat())

    def test_entities_dict_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        entities = handler._entities()
        # assert
        self.assertIsInstance(entities, dict)

    def test_entities_empty_msg(self):
        # arrange
        message = dict(self.valid_message['message'])
        del message['entities']
        message = {'message': message}

        handler = UpdatesHandler.factory(message)
        # act
        entities = handler._entities()
        # assert
        self.assertEqual(entities, {})

    def test_entities_empty_cd(self):
        # arrange
        handler = self.get_CallbackDTO()
        # act
        entities = handler._entities()
        # assert
        self.assertEqual(entities, {})

    def test_is_command_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        # assert
        self.assertTrue(handler.is_command())

    def test_is_command_cb(self):
        # arrange
        handler = self.get_CallbackDTO()
        # act
        # assert
        self.assertTrue(handler.is_command())

    def test_get_phrase_cb(self):
        # arrange
        handler = self.get_CallbackDTO()
        # act
        phrase = handler.get_phrase()
        # assert
        self.assertEqual(phrase, 'recognize')

    def test_get_phrase_msg(self):
        # arrange
        handler = self.get_MessageDTO()
        # act
        phrase = handler.get_phrase()
        # assert
        self.assertEqual(phrase, 'recognize')

    def test_phrase_identical(self):
        # arrange
        msg_handler = self.get_MessageDTO()
        cb_handler = self.get_CallbackDTO()
        # act
        msg_phrase = msg_handler.get_phrase()
        cb_phrase = cb_handler.get_phrase()
        # assert
        self.assertEqual(msg_phrase, cb_phrase)


if __name__ == '__main__':
    unittest.main()
