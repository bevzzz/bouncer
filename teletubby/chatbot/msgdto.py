from teletubby.actors.owner import Owner


class UpdatesHandler:

    @staticmethod
    def factory(update):
        handler = UpdatesHandler()

        if update.get('message', False):
            handler = MessageDTO(update['message'])

        elif update.get('callback_query', False):
            handler = CallbackDTO(update['callback_query'])

        return handler


class MessageDTO(UpdatesHandler):
    """
    MessageDTO works with responses from Telegram API. It receives a "message" JSON
    from Conversation and extracts key features of the message: text, attachments and
    attachment mime_types if such exist etc.
    """

    def __init__(self, message):
        self.message = message
        self.read = False
        self.author = Owner.get_instance(self._from())

    def is_read(self):
        return self.read

    def mark_as_read(self):
        self.read = True

    def get_author(self):
        return self.author

    # from
    def _from(self):
        return self.message['from']

    # chat
    def _chat(self):
        return self.message['chat']

    def get_chat_id(self):
        chat = self._chat()
        chat_id = chat['id']
        return str(chat_id)

    def is_private_chat(self):
        chat = self._chat()
        return chat['type'] == 'private'

    # message
    def get_message_id(self):
        return self.message['message_id']

    def _entities(self):
        return self.message.get('entities', '')

    def _is_command(self):
        try:
            entity = self._entities()[0]
            res = entity['type'] == 'bot_command'
        except KeyError:
            # log 'message has no entities'
            res = False
        except IndexError:
            # log 'empty "entities" list'
            res = False

        return res

    def is_predefined(self):
        return self._is_command()

    def get_phrase(self):
        return self.message.get('text', '')

    # attachments
    def has_photo(self):
        return self._attachment_mime_type() == 'image/jpeg'

    def _attachment_mime_type(self):
        if self._photo_as_photo():
            mime_type = 'image/jpeg'
        elif self._photo_as_document():
            mime_type = self.message['document']['mime_type']
        else:
            mime_type = ''

        return mime_type

    def _photo_as_photo(self):
        return self.message.get('photo', False)

    def _photo_as_document(self):
        return self.message.get('document', False)

    def get_picture_with_caption(self):
        file_id = ''
        if self._photo_as_photo():
            file_id += self._get_small_photo_file_id()
        elif self._photo_as_document():
            file_id += self._get_document_file_id()
        caption = self.message.get('caption', '')
        return file_id, caption

    def _get_document_file_id(self):
        return self.message['document']['file_id']

    def _get_small_photo_file_id(self):
        return self.message['photo'][0]['file_id']


class CallbackDTO(MessageDTO):

    def __init__(self, callback_query):
        self.callback_query = callback_query
        self.author = Owner.get_instance(self._from())
        super().__init__(self._message())

    def _from(self):
        return self.callback_query['from']

    def _message(self):
        return self.callback_query['message']

    def get_phrase(self):
        return self.callback_query.get('data', '')

    def is_predefined(self):
        return True


