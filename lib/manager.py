# from lib.chatbot.reaction.reactionFactory import ReactionFactory
# from lib.chatbot.conversation import Conversation
from lib.chatbot.state.conversationContext import ConversationContext
from lib.chatbot.state.UpdateParser import UpdateParser
import logging
import time
import base64
import requests


class Manager:

    def __init__(self, chatbot, storage):
        self.chatbot = chatbot
        self.storage = storage
        self.conversations = []
        self.log = logging.getLogger()

    # def talk(self):
    #     self.log.info("start talk()")
    #
    #     while True:
    #
    #         conversations = self._update_conversations()
    #         for conv in conversations:
    #             for msg in conv.get_new_messages():
    #                 # self._react_to_message(msg)
    #                 self._react_to_msg(msg)
    #
    #         self.chatbot.update_offset()
    #
    #         time.sleep(1)
    #
    # def _update_conversations(self):
    #     updates = self.chatbot.get_updates()
    #     conversations = Conversation.open_conversations(updates)
    #
    #     for conv in conversations:
    #         self.conversations.append(conv)
    #
    #     return conversations
    #
    # def _react_to_message(self, message):
    #     reaction = ReactionFactory(self).get(
    #         message=message
    #     )
    #     reaction.action()
    #     reaction.response()
    #     message.mark_as_read()
    #
    # def _react_to_msg(self, msg):
    #     if msg.has_photo():
    #         file_id = msg.get_file_id()
    #         photo = self.chatbot.download_file(file_id)
    #     else:
    #         photo = None
    #
    #     # TODO: get previous message
    #     state = Conversation.get_previous_message(msg).get_phrase()
    #
    #     r = ReactionFactory(self).get(
    #         message=msg,
    #         photo=photo,
    #         state=state
    #     )
    #
    #     r.take_action()
    #     response = r.get_response()
    #     self._update_message(
    #         old_msg=msg,
    #         new_msg=response
    #     )
    #
    # def _update_message(self, old_msg, new_msg):
    #
    #     self.chatbot.delete_message(
    #         chat_id=old_msg.get_chat_id(),
    #         message_id=old_msg.get_message_id()
    #     )
    #     self.chatbot.send_message(new_msg)

    def talk(self):
        self.log.info("start talk()")

        while True:
            updates = self.chatbot.get_updates()

            for update in updates:

                try:
                    update = UpdateParser.factory(update)
                    self.log.info(
                        f"new message from {update.get_author().get_username()}"
                    )

                    conversation = ConversationContext.open(self, update)
                    conversation.reply()

                except LookupError as err:
                    self.log.warning(err)

            self.chatbot.update_offset()

    def update_message(self, chat_id, to_delete_id, to_send):
        self.log.info(
            f"update_message(): \n"
            f"deleting: {to_delete_id} \n"
            f"sending: {to_send}"
        )

        self.chatbot.delete_message(
            chat_id=chat_id,
            message_id=to_delete_id
        )
        return self.chatbot.send_message(to_send)

    def get_user_roles(self):
        self.storage.set_root_path('')
        user_roles = self.storage.read_json('config', 'users.json')
        self.storage.set_root_path('images')

        return user_roles

    def is_authorized_user(self, user):
        user_roles = self.get_user_roles()
        return user.get_username() in list(user_roles.keys())

    def is_admin(self, user):
        user_roles = self.get_user_roles()
        return user_roles[user.get_username()] == 'admin'

    @staticmethod
    def send_request_to_recognize(img):
        base_url = 'http://localhost:5000/bouncer/v1/model/recognize'
        img = base64.encodebytes(img).decode('utf-8')

        body_json = {
            'img': img
        }

        response = requests.post(url=base_url, json=body_json)
        return response.json()

    def send_request_to_train(self, people=None):
        # TODO: probably I should use facerec:5000 when running this from docker-compose
        base_url = 'http://localhost:5000/bouncer/v1/model/train'

        if people is None:
            people = self.get_user_roles()
            people = list(people.keys())

        body_json = {
            'people': people
        }

        response = requests.post(url=base_url, json=body_json)
        return response.json()

