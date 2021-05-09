
class Chat:

    _instance = {}

    def __init__(self, chat_id):
        self.messages = {}
        self.state = None
        self._instance[chat_id] = self

    @classmethod
    def get_instance(cls, chat_id):
        if chat_id in cls._instance:
            return cls._instance[chat_id]
        else:
            cls(chat_id)

    def add_message(self, message):
        self.messages = {
            message.get_id(): message
        }
        # TODO: change state according to the message

    def get_state(self):
        return self.state

