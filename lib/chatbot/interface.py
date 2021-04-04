from abc import ABCMeta, abstractmethod
import logging


class Chatbot(metaclass=ABCMeta):

    def __init__(self):
        self.log = logging.getLogger()

    @abstractmethod
    def get_updates(self):
        pass

    @abstractmethod
    def download_file(self, file):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def send_file(self, file, chat_id):
        pass
