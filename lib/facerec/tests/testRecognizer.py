# Build-in libraries
import os

# Third-party libraries
import unittest
import numpy as np
from PIL import Image

# Local libraries
from lib.facerec.recognize import Recognizer
from lib.facerec.encode import Encoder


class TestRecognizer(unittest.TestCase):

    test_img_path = "/home/dmytro/pycharm/bouncer/lib/facerec/tests/bin/dannydevito.png"

    @classmethod
    def setUpClass(cls):
        cls.r = Recognizer(testing=True)

    def tearDown(self):
        self.r.set_known({"names": None, "encodings": None})

    def get_encodings(self, name, path=""):
        e = Encoder()
        imgb = self.get_bytes_image(path)
        arr = self.r._prepare_for_encoding(imgb)
        enc = e.encode(arr)

        return name, enc

    def get_known_list(self, ntrue=1, nfalse=1):
        nd, encd = self.get_encodings("Danny Devito")
        na, enca = self.get_encodings("Arnold", "/home/dmytro/pycharm/bouncer/lib/facerec/tests/bin/schwarz.jpg")
        names = [nd]*ntrue + [na]*nfalse
        encodings = encd*ntrue + enca*nfalse
        return {"encodings": encodings, "names": names}

    def get_bytes_image(self, path=""):
        if path == "":
            path = self.test_img_path
        with open(path, 'rb') as b:
            return b.read()

    def get_pil_image(self):
        return Image.open(self.test_img_path)

    def test_convert_PIL_image_to_array(self):
        # arrange
        img = self.get_pil_image()
        # act
        got = self.r._convert_pil_to_array(img)
        # assert
        self.assertIsInstance(got, np.ndarray)

    def test_convert_bytes_to_pil(self):
        # arrange
        imgb = self.get_bytes_image()
        # act
        img = self.r._convert_bytes_to_pil(imgb)
        # assert
        self.assertIsInstance(img, Image.Image)

    def test_is_RGB(self):
        # arrange
        img_not_rgb = self.get_pil_image()
        img_rgb = img_not_rgb
        # act
        img_rgb = img_rgb.convert("RGB")
        # assert
        self.assertTrue(self.r._is_rgb(img_rgb))
        self.assertFalse(self.r._is_rgb(img_not_rgb))

    def test_prepare_for_encoding(self):
        # arrange
        imgb = self.get_bytes_image()
        # act
        arr = self.r._prepare_for_encoding(imgb)
        # assert
        self.assertIsInstance(arr, np.ndarray)

    def test_set_encodings(self):
        # arrange
        enc = self.get_known_list()
        # act
        self.r.set_known(enc)
        # assert
        self.assertIsNotNone(self.r._encodings)

    def test_finds_a_match(self):
        # arrange
        imgb = self.get_bytes_image()
        arr = self.r._prepare_for_encoding(imgb)
        e = Encoder()
        encoded_img = e.encode(arr)
        known_encodings = self.get_known_list()
        self.r.set_known(known_encodings)
        # act
        matched = self.r._find_matches(encoded_img[0])
        # assert
        self.assertTrue(matched[0])

    def test_determines_match(self):
        # arrange
        matches = [True, True, True, False, False, True, False, False, False, False]
        known_encodings = self.get_known_list(ntrue=4, nfalse=6)
        self.r.set_known(known_encodings)
        # act
        person, reason = self.r._determine_the_match(matches)
        # assert
        self.assertEqual(person, "Danny Devito")

    def test_recognize_returns_none_if_none_known(self):
        # arrange
        imgb = self.get_bytes_image()
        # act
        person = self.r.recognize(imgb)
        # assert
        self.assertIsNone(person.username)

    def recognizes_danny(self):
        # arrange
        imgb = self.get_bytes_image()
        known_encodings = self.get_known_list()
        self.r.set_known(known_encodings)
        # act
        person = self.r.recognize(imgb)
        # assert
        self.assertEqual(person.username, "Danny Devito")

    def test_dont_train_with_unknown_names(self):
        # arrange
        for_names = ["bevzzz", "testname"]
        # act
        ok = self.r.train(for_names)
        # assert
        self.assertFalse(ok)

    def test_train_saves_new(self):
        # arrange
        for_names = ["bevzzz"]
        # act
        ok = self.r.train(
            names=for_names,
            save_new=True
        )
        # assert
        self.assertTrue(ok)
        self.assertTrue(os.path.exists("/home/dmytro/pycharm/bouncer/resources/model/encodings.pickle"))

    def test_sets_known(self):
        # arrange
        for_names = ["bevzzz"]
        # act
        ok = self.r.train(
            names=for_names,
            set_new=True
        )
        # assert
        known = self.r.known
        self.assertEquals(for_names[0], set(known["names"]).pop())
