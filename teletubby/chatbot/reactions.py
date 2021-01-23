from teletubby.chatbot.telegram_object import InlineKeyboardButton, InlineKeyboardMarkup, TextMessage, KeyboardButton, ReplyKeyboardMarkup
from teletubby.chatbot.conversation import Conversation
from teletubby.tools.img import IMG
from teletubby.tools import imagetools


class Reaction:

    def __init__(self, me, message):
        self.me = me
        self.message = message

    @classmethod
    def factory(cls, me, message):
        reaction = Reaction(me, message)

        phrase = message.get_phrase()
        last_message = Conversation.get_previous_message(message)

        if message.has_photo():
            reaction = ReactionPhoto(me, message)
        else:
            if phrase == '/start':
                reaction = ReactionStart(me, message)
            elif phrase == 'authorize' or phrase == 'stay_guest':
                reaction = ReactionAskPassword(me, message)
            elif last_message.get_phrase() == 'authorize':
                reaction = ReactionAuthorization(me, message)

        return reaction

    def response(self):
        text = "Ufff... I'm speechless"
        message_out = TextMessage(text=text)
        self._send_message(message_out)

    def action(self):
        pass

    def _send_message(self, message_out):
        message_out['chat_id'] = self.message.get_chat_id()
        message_out = message_out.to_dict()
        self.me.send_message(message_out)

    def _send_picture(self, picture_out, chat_id):
        self.me.send_file_to_chat(picture_out, chat_id)

    def _turn_off_inline_keyboard(self, inline_message_id=None, chat_id=None, message_id=None):
        message_out = TextMessage(text=None)

        if inline_message_id is not None:
            message_out['inline_message_id'] = inline_message_id
        elif chat_id is not None and message_id is not None:
            message_out['chat_id'] = chat_id
            message_out['message_id'] = message_id

        message_out = message_out.to_dict()
        self._send_message(message_out)


class ReactionStart(Reaction):

    def __init__(self, me, message):
        super().__init__(me, message)

    def response(self):
        author = self.message.get_author()
        text = 'Hi, {}!\n'.format(author.get_name())

        if author.ask_to_authorize():

            enquiry = "You haven't authorized with me yet.\n" \
                      "Tap 'Authorize' below or choose to proceed as a Guest"

            reply_markup = self._build_reply_keyboard()

        else:
            enquiry = "How can I be of service?"
            reply_markup = None

        text += enquiry
        message_out = TextMessage(text=text, reply_markup=reply_markup)

        self._send_message(message_out)

    @staticmethod
    def _build_inline_markup():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Authorize', callback_data='authorize')],
            [InlineKeyboardButton('Proceed as a Guest', callback_data='stay_guest')]
        ])

    @staticmethod
    def _build_reply_keyboard():
        return ReplyKeyboardMarkup([
            [KeyboardButton('authorize')],
            [KeyboardButton('stay_guest')]
        ])


class ReactionAskPassword(Reaction):

    def __init__(self, me, message):
        super().__init__(me, message)

    def response(self):
        owner = self.message.get_author()
        if self._stays_guest():
            text = "Very well, I shall call you Guest {}".format(owner.first_name)
        else:
            text = "Haha! I guess my master has imparted his secret phrase to you!\n" \
                   "What is it?"

        message_out = TextMessage(text=text)
        self._send_message(message_out)

    def action(self):
        owner = self.message.get_author()
        if self._stays_guest():
            owner.set_ask_to_authorize_false()

    def _stays_guest(self):
        return self.message.get_phrase() == 'stay_guest'


class ReactionAuthorization(Reaction):

    def __init__(self, me, message):
        super().__init__(me, message)

    def response(self):
        owner = self.message.get_author()
        if self._password_correct():
            text = "Yep, that's right!\n" \
                   "Now, {}, how can I be of service?".format(owner.first_name)
        else:
            text = "No, not really ;(\n" \
                   "Tap 'authorize' to try again or fuck off"
            # offer to try again

        message_out = TextMessage(text=text)
        self._send_message(message_out)

    def action(self):
        if self._password_correct():
            owner = self.message.get_author()
            owner.make_a_friend()
        else:
            # offer to try again
            pass

    def _password_correct(self):
        user_password = self.message.get_phrase().upper()
        correct_password = self.me.secret_password
        return user_password == correct_password


class ReactionPhoto(Reaction):

    def __init__(self, me, message):
        super().__init__(me, message)
        self.upload_successful = False

    def response(self):
        if self.upload_successful:
            text = "That's some goodie-goodie-good good old stuff!\n" \
                   "I've put in on Drive for you, *wink*"
        else:
            text = "Oh crap, something went wrong - I couldn't upload it...\n" \
                   "Please contact Mr. Bevz for support"

        message_out = TextMessage(text=text)
        self._send_message(message_out)

    def action(self):
        file_id, caption = self.message.get_picture_with_caption()
        owner = self._get_photo_owner(caption)
        folder_id = self._get_folder_id(owner)

        bytes_array = self._download_bytes_photo(file_id)
        photo = IMG(bytes_array, owner)

        detected_faces = imagetools.extract_resized_faces(photo.as_ndarray())
        for face_img in detected_faces:
            self._send_picture(face_img, self.message.get_chat_id())
            photo_up = IMG(face_img, owner)
            file_id = self.me.upload_to_drive(photo_up, folder_id)
            if file_id:
                self.upload_successful = True

    def _download_bytes_photo(self, file_id):
        return self.me.chatbot.download_file(file_id)

    def _get_folder_id(self, owner):
        return self.me.drive.get_folder_id_by_name(owner.username)

    def _get_photo_owner(self, caption):
        if caption:
            # owner = Owner(caption)
            # should be possible to create an Owner with just a username
            # Owner needs a major rework
            owner = self.message.get_author()
        else:
            owner = self.message.get_author()
        return owner
