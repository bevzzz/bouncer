import io
import numpy as np
from PIL import Image
from matplotlib import pyplot
from teletubby.tools import helpers
from googleapiclient.http import MediaIoBaseUpload


class File:
    pass


class IMG(File):

    mime_type = 'image/jpeg'

    def __init__(self, body, owner=None):
        self.body = body
        if owner is not None:
            self.owner = owner
            self.name = self._build_name()
        self.drive_id = None

    def _build_name(self):
        return '{}_{}'.format(self.owner.username, helpers.get_timestamp())

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def set_owner(self, owner):
        self.owner = owner
        self.name = self._build_name()

    def get_upload_media(self):
        io_body = self.get_io_buffer()
        media = MediaIoBaseUpload(
            fd=io_body,
            mimetype=self.mime_type,
            chunksize=self.get_size()
        )
        return media

    def get_io_buffer(self):
        return io.BytesIO(self.body)

    def get_size(self):
        return len(self.body)

    def as_ndarray(self):
        buffer = self.get_io_buffer()
        img = Image.open(buffer)
        return np.array(img)




