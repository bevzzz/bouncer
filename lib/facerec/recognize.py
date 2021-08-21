# Built-in libraries
import io
import os
import pickle

import numpy as np

# Third-party libraries
import face_recognition
from PIL import Image

# Local libraries
from lib.facerec.encode import Encoder
from lib.model.person import Person


RGB = "RGB"


class Recognizer:

    _image_dir = os.path.join("/home/dmytro/pycharm/bouncer/resources/images/")
    _encodings_dir = os.path.join("/home/dmytro/pycharm/bouncer/resources/model/")

    def __init__(self, known=None, method='hog', tolerance=0.6, testing=False):

        self._names = None
        self._encodings = None

        if known is not None:
            self.set_known(known)

        self.method = method
        self.tolerance = tolerance
        self.encoder = Encoder(self.method)

        self._testing = testing

    @property
    def known(self):
        return {
            "encodings": self._encodings,
            "names": self._names
        }

    def set_known(self, known):
        self._names = known["names"]
        self._encodings = known["encodings"]

    def clear_known(self):
        self._names = None
        self._encodings = None

    @staticmethod
    def _convert_pil_to_array(img):
        return np.array(img)

    @staticmethod
    def _convert_bytes_to_pil(img_bytes):
        b = io.BytesIO(img_bytes)
        return Image.open(b)

    @staticmethod
    def _is_rgb(img):
        return img.mode == RGB

    @staticmethod
    def _convert_to_rgb(img):
        return img.convert(RGB)

    def _prepare_for_encoding(self, img_bytes):
        img = self._convert_bytes_to_pil(img_bytes)
        if not self._is_rgb(img):
            img = self._convert_to_rgb(img)
        return self._convert_pil_to_array(img)

    def _find_matches(self, encoded_img):
        return face_recognition.compare_faces(
            known_face_encodings=self._encodings,
            face_encoding_to_check=encoded_img,
            tolerance=self.tolerance
        )

    def _determine_the_match(self, matches):
        name_out = ""
        if True in matches:
            matched_idx = [i for (i, match) in enumerate(matches) if match]
            counts = {}
            for i in matched_idx:
                name = self._names[i]
                counts[name] = counts.get(name, 0) + 1

            name_out = max(counts, key=counts.get)
        return name_out, ""

    def recognize(self, img_bytes):

        if self._encodings is None or self._names is None:
            return Person()

        arr = self._prepare_for_encoding(img_bytes)
        encoded_img = self.encoder.encode(arr)

        if len(encoded_img) > 1:
            raise RuntimeError("Images with multiple faces are not supported")

        matches = self._find_matches(encoded_img[0])
        name, reason = self._determine_the_match(matches)

        return Person(name)

    def train(self, names, save_new=False, set_new=False):

        existing_folders = os.listdir(self._image_dir)
        if not all(n in existing_folders for n in names):
            return False

        # initialize lists for encodings
        known_encodings = []
        known_names = []

        for n in names:

            dir_path = os.path.join(self._image_dir, n)
            images = os.listdir(dir_path)

            for img in images:
                img_path = os.path.join(self._image_dir, n, img)
                with open(img_path, "rb") as b:
                    img_bytes = b.read()
                    arr = self._prepare_for_encoding(img_bytes)
                    encoded_img = self.encoder.encode(arr)

                    for e in encoded_img:
                        known_encodings.append(e)
                        known_names.append(n)

        known = {
            "encodings": known_encodings,
            "names": known_names
        }

        if save_new:

            if self._testing:
                filename = "encodings_test.pickle"
            else:
                filename = "encodings.pickle"

            path = os.path.join(self._encodings_dir, filename)
            with open(path, "wb") as wb:
                pickle.dump(known, wb)

        if set_new:
            self.set_known(known)

        return True
