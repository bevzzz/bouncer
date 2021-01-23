import requests


class TelegramAPI:
    """
    A nice Telegram API client
    """

    host_url = 'https://api.telegram.org'

    def __init__(self, token):
        self.token = token
        self.base_url = self._build_base_url()
        self.identity = self.get_me()
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

    def get_updates(self):
        req = self._build_request('getUpdates')
        params = {'offset': self.offset}
        response = requests.get(req, params).json()
        self.updates = response.get('result', [])
        return self.updates

    def update_offset(self):
        try:
            self.offset = self.updates[-1]['update_id'] + 1
        except IndexError:
            print('No fresh updates')

    def get_file(self, file_id):
        req = self._build_request('getFile')
        params = {'file_id': file_id}
        response = requests.get(req, params).json()
        file_path = response['result']['file_path']
        return file_path

    def send_message(self, body):
        req = self._build_request('sendMessage')
        requests.post(req, body).json()

    def download_file(self, file_id):
        file_path = self.get_file(file_id)
        req = self._build_download_request(file_path)
        byte_array = requests.get(req).content
        return byte_array

    def upload_file(self, file, chat_id):
        req = self._build_request('sendPhoto')
        data = {
            'chat_id': chat_id
        }
        files = {
            'photo': file
        }
        print(requests.post(req, data=data, files=files).json())

