import unittest

import face_recognition
from PIL import Image
import numpy as np
import lib.facerec.encode as e


class TestEncode(unittest.TestCase):

    test_img_path = "/lib/facerec/tests/bin/dannydevito.png"

    @classmethod
    def setUpClass(cls):
        cls.encoder = e.Encoder()

    def get_test_image(self):
        im = Image.open(self.test_img_path).convert("RGB")
        return np.array(im)

    def test_locate_faces(self):
        # arrange
        want = [(82, 311, 211, 182)]
        arr = self.get_test_image()
        # act
        boxes = self.encoder.locate(arr)
        # assert
        self.assertEqual(boxes, want)

    def test_encode_one(self):
        # arrange
        arr = self.get_test_image()
        boxes = face_recognition.face_locations(arr, model='hog')
        want = face_recognition.face_encodings(arr, boxes)
        # act
        got = self.encoder.encode(arr)
        # assert
        self.assertTrue(np.array_equal(got, want))


if __name__ == '__main__':
    unittest.main()
