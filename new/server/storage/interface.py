from abc import ABCMeta, abstractmethod
import logging


class Storage(metaclass=ABCMeta):

    def __init__(self):
        self.log = logging.getLogger()

    @abstractmethod
    def _write_image(self, img, name, to_dir):
        pass

    @abstractmethod
    def _read_image(self, name, from_dir):
        pass

    @abstractmethod
    def _create_folder(self, name):
        pass

    @abstractmethod
    def _list_folders(self):
        pass

    def _folder_exists(self, my_folder):
        all_folders = self._list_folders()
        return any(f == my_folder for f in all_folders)
