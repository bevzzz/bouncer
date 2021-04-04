from telegram import ReplyKeyboardMarkup
from lib.chatbot.interface import Chatbot
import requests
import logging


class TelegramBot(Chatbot):

    host_url = 'https://api.telegram.org'

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.base_url = self._build_base_url()
        self.offset = 0
        self.updates = {}

    def _build_base_url(self):
        return '{}/bot{}'.format(self.host_url, self.token)

    def _build_request(self, method):
        return '{}/{}'.format(self.base_url, method)

    def _build_download_request(self, file_path):
        return '{}/file/bot{}/{}'.format(self.host_url, self.token, file_path)

    def get_me(self):
        req = self._build_request('getMe')
        response = requests.get(req).json()
        return response['result']

    def update_offset(self):
        try:
            self.offset = self.updates[-1]['update_id'] + 1
            self.log.info(self.updates[-1])
        except IndexError:
            pass

    def get_updates(self):
        req = self._build_request('getUpdates')
        params = {'offset': self.offset}
        response = requests.get(req, params).json()
        self.updates = response.get('result', [])
        return self.updates

    def _get_file(self, file_id):
        req = self._build_request('getFile')
        params = {'file_id': file_id}
        response = requests.get(req, params).json()
        file_path = response['result']['file_path']
        return file_path

    def download_file(self, file_id):
        file_path = self._get_file(file_id)
        req = self._build_download_request(file_path)
        byte_array = requests.get(req).content
        return byte_array

    def send_message(self, message_body):
        req = self._build_request('sendMessage')
        requests.post(req, message_body).json()

    def send_file(self, file, chat_id):
        req = self._build_request('sendPhoto')
        data = {
            'chat_id': chat_id
        }
        files = {
            'photo': file
        }
        requests.post(req, data=data, files=files).json()