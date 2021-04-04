import json


class TelegramObject:

    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        return data


class TextMessage(TelegramObject):

    def __init__(self, text, chat_id=None, reply_markup=None):
        self.text = text
        self.chat_id = chat_id
        self.reply_markup = reply_markup

    def to_dict(self):
        data = super().to_dict()
        if self.reply_markup is not None:
            reply_markup = self.reply_markup.to_dict()
            data['reply_markup'] = json.dumps(reply_markup)
        return data


class InlineKeyboardButton(TelegramObject):

    def __init__(
            self,
            text,
            url=None,
            login_url=None,
            callback_data=None
    ):
        self.text = text
        self.url = url
        self.login_url = login_url
        self.callback_data = callback_data
        super().__init__()


class InlineKeyboardMarkup(TelegramObject):

    def __init__(self, inline_keyboard):
        self.inline_keyboard = inline_keyboard

    def to_dict(self):
        data = super().to_dict()

        data['inline_keyboard'] = []
        for inline_keyboard in self.inline_keyboard:
            data['inline_keyboard'].append([x.to_dict() for x in inline_keyboard])

        return data


class KeyboardButton(TelegramObject):

    def __init__(
            self,
            text,
            request_contact=None,
            request_location=None,
            request_pole=None
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_pole = request_pole


class ReplyKeyboardMarkup(TelegramObject):

    def __init__(
            self,
            keyboard,
            resize_keyboard=False,
            one_time_keyboard=True,
            selective=False
    ):
        self.keyboard = []
        for row in keyboard:
            button_row = []
            for button in row:
                if isinstance(button, KeyboardButton):
                    button_row.append(button)
                else:  # passed as string
                    button_row.append(KeyboardButton(button))
            self.keyboard.append(button_row)

        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

    def to_dict(self):
        data = super().to_dict()

        data['keyboard'] = []
        for row in self.keyboard:
            button_row = [button.to_dict() for button in row]
            data['keyboard'].append(button_row)

        return data
