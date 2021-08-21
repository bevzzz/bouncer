import io

import face_recognition
import numpy as np
from PIL import Image
from lib.facerec.encode import Encoder


RGB = "RGB"


class Recognizer:

    def __init__(self, known=None, method='hog', tolerance=0.6):

        self._names = None
        self._encodings = None

        if known is not None:
            self.set_known(known)

        self.method = method
        self.tolerance = tolerance
        self.encoder = Encoder(self.method)

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
            return None

        arr = self._prepare_for_encoding(img_bytes)
        encoded_img = self.encoder.encode(arr)
        matches = self._find_matches(encoded_img)
        name, reason = self._determine_the_match(matches)

        # return person