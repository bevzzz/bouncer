import os
import json
import pickle
from lib.storage.interface import Storage


class LocalStorage(Storage):

    def __init__(self, root_path='images'):
        self.root_path = os.path.join(
            os.getcwd(),
            'resources',
            root_path
        )
        super().__init__()

    def set_root_path(self, root_path):
        self.root_path = os.path.join(
            os.getcwd(),
            'resources',
            root_path
        )

    def _build_filepath(self, directory='', *args):

        return os.path.join(
            self.root_path,
            directory,
            *args
        )

    def list_directory(self, name=None):
        if name is None:
            filepath = self._build_filepath()
        else:
            filepath = self._build_filepath(name)
        return os.listdir(filepath)

    def is_empty_dir(self, path):
        return self.list_directory(path) == []

    def create_directory(self, name):

        if not self.exists_directory(name):
            self.log.info(f"Directory {name} didn't exist, adding")
            filepath = self._build_filepath(name)
            os.mkdir(filepath)

    def _read_file(self, from_dir, name, func):
        filepath = self._build_filepath(from_dir, name)

        with open(filepath, 'rb') as from_file:
            return func(
                from_file.read()
            )

    def read_image(self, from_dir, name):
        return self._read_file(
            from_dir,
            name,
            func=lambda i_o: i_o
        )

    def read_json(self, from_dir, name):
        return self._read_file(
            from_dir,
            name,
            func=lambda i_o: json.loads(i_o)
        )

    def read_pickle(self, from_dir, name):
        return self._read_file(
            from_dir,
            name,
            func=lambda i_o: pickle.loads(i_o)
        )

    def _write_file(self, file, name, to_dir, func):
        filepath = self._build_filepath(to_dir, name)
        with open(filepath, 'wb') as to_file:
            to_file.write(
                func(file)
            )

    def write_image(self, img, name, to_dir=None):
        self.log.info(f'Saving new image of {to_dir}')

        self.create_directory(to_dir)
        self._write_file(
            img,
            name,
            to_dir,
            func=lambda f: f
        )

    def write_json(self, file, name, to_dir=None):
        self.log.info(f"Writing JSON: {name}")

        self._write_file(
            file,
            name,
            to_dir,
            func=lambda f: json.dumps(f)
        )

    def write_pickle(self, file, name, to_dir=None):
        self.log.info(f"Writing pickle: {name}")

        self._write_file(
            file,
            name,
            to_dir,
            func=lambda f: pickle.dumps(f)
        )
