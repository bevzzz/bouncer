from abc import ABCMeta, abstractmethod
import logging


class Storage(metaclass=ABCMeta):

    def __init__(self):
        self.log = logging.getLogger("Storage")

    @abstractmethod
    def write_image(self, img, name, to_dir):
        pass

    @abstractmethod
    def read_image(self, name, from_dir):
        pass

    @abstractmethod
    def create_directory(self, name):
        pass

    @abstractmethod
    def list_directory(self, name=None):
        pass

    def exists_directory(self, my_dir):
        all_dirs = self.list_directory()
        return any(f == my_dir for f in all_dirs)
