from new.server.storage.interface import Storage
import os
import cv2
import json


class LocalStorage(Storage):

    def write_jpeg(self, img, name, to_dir):
        name = '{}.jpeg'.format(name)
        return self._write_image(img, name, to_dir)

    def read_jpeg(self, name, from_dir):
        name = '{}.jpeg'.format(name)
        return self._read_image(name, from_dir)

    def _write_image(self, img, name, to_dir=''):
        self.log.info("new _write_image(), user " + to_dir)

        if not self._folder_exists(to_dir):
            self._create_folder(to_dir)

        filepath = self._build_filepath('pictures', to_dir, name)
        with open(filepath, 'wb') as to_file:
            to_file.write(img)

    def _read_image(self, name, from_dir=''):

        filepath = self._build_filepath('pictures', from_dir, name)
        return cv2.imread(filepath)

    def _create_folder(self, name):
        filepath = self._build_filepath('pictures', name)
        os.mkdir(filepath)

    def _list_folders(self):
        filepath = self._build_filepath('pictures')
        return os.listdir(filepath)

    @staticmethod
    def _build_filepath(directory='pictures', *args):
        return os.path.join(
            os.getcwd(),
            'new/server',
            directory,
            *args
        )

    def read_config_json(self, name):
        filepath = self._build_filepath('config', name)
        with open(filepath) as json_file:
            return json.load(json_file)
