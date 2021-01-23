import teletubby.chatbot.reactions as r
from teletubby.chatbot.conversation import Conversation


class Manager:
    """
    Dvoretski (Manager) is the central figure in the program, the brain, the doorman, Konstantin himself.
    There exist several Owners, who own DrivePictures and other DriveFiles stored in GoogleDrive folders.
    Dvoretski knows them and talks to them through TelegramAPI, saving their messages in Conversations.
    Dvoretski also uploads and downloads DriveFiles from/to Storages. Dvoretski can pass a picture to Machine
    and call upon Door to allow someone in the apartment.
    """

    friends = ['jkorbut', 'mnmosine', 'bevzzz']
    secret_password = 'WARHOL BIS RICHTER'

    def __init__(self, chatbot, drive):
        self.chatbot = chatbot
        self.drive = drive
        self.conversations = []

    def talk(self):
        conversations = self._update_conversations()
        for conv in conversations:
            for msg in conv.get_new_messages():
                self._react_to_message(msg)

        self.chatbot.update_offset()

    def _update_conversations(self):
        updates = self.chatbot.get_updates()
        print(updates)
        conversations = Conversation.open_conversations(updates)

        for conv in conversations:
            self.conversations.append(conv)

        return conversations

    def _react_to_message(self, message):
        reaction = r.Reaction.factory(self, message)
        reaction.action()
        reaction.response()
        message.mark_as_read()

    def upload_to_drive(self, file, folder_id):
        drive_id = self.drive.upload_file(file, folder_id)
        file.drive_id = drive_id
        return drive_id

    def send_message(self, message):
        self.chatbot.send_message(message)

    def send_file_to_chat(self, file, chat_id):
        self.chatbot.upload_file(file, chat_id)

