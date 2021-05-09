from lib.chatbot.state.conversationContext import ConversationContext
from lib.chatbot.state.UpdateParser import UpdateParser


def conversation_caller(update):

    update = UpdateParser.factory(update)
    conversation = ConversationContext(self, update)
    conversation.reply()


def _update_message(self, to_delete, to_send):

    self.chatbot.delete_message(
        chat_id=to_delete.get_chat_id(),
        message_id=to_delete.get_message_id()
    )
    self.chatbot.send_message(to_send)
