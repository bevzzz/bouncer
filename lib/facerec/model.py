import numpy as np
from PIL import Image as im
import face_recognition
from io import BytesIO


class Model:

    def __init__(self, encodings=None, method='hog'):

        self.method = method

        if encodings is not None:
            self.known_encodings = encodings.get('encodings', [])
            self.known_names = encodings.get('names', [])
        else:
            self.encodings = encodings

    def train(self, train_set):

        knownNames = []
        knownEncodings = []

        for key, values in train_set.items():

            for img in values:

                img = self._from_bytes_to_pil_image(img)
                encodings = self._get_encodings(np.array(img))

                for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(key)

        encodings_data = {
            "encodings": knownEncodings,
            "names": knownNames
        }

        return encodings_data

    def recognize(self, img):
        """
        Recognizes the face on the picture
        :param img: bytes-array image
        :return: name of the person in the picture
        """

        img = self._from_bytes_to_pil_image(img)

        if not self._is_RGB(img):
            self._convert_to_RGB(img)
        img = np.array(img)

        encoded_faces = self._get_encodings(img)
        names = []
        for face in encoded_faces:
            matches = self._find_matches(face)
            names.append(self._get_most_probable_name(matches))

        return names

    @staticmethod
    def _from_bytes_to_pil_image(img):
        buffer = BytesIO(img)
        return im.open(buffer)

    @staticmethod
    def _is_RGB(img):
        return img.mode == 'RGB'

    @staticmethod
    def _convert_to_RGB(img):
        return img.convert('RGB')

    def _get_encodings(self, img):
        boxes = self._locate_faces(img)
        return self._encode(img, boxes)

    def _locate_faces(self, img):
        return face_recognition.face_locations(
            img=img,
            model=self.method
        )

    @staticmethod
    def _encode(img, boxes):
        return face_recognition.face_encodings(
            face_image=img,
            known_face_locations=boxes
        )

    def _find_matches(self, encoded_face):
        return face_recognition.compare_faces(
            self.known_encodings,
            encoded_face
        )

    def _get_most_probable_name(self, matches, tolerance=0.5):
        name_out = 'Unknown'
        if True not in matches:
            return name_out
        else:
            matched_idx = [i for (i, match) in enumerate(matches) if match]

            counts = {}
            for i in matched_idx:
                name = self.known_names[i]
                counts[name] = counts.get(name, 0) + 1

            return max(counts, key=counts.get)


