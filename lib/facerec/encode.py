import face_recognition


class Encoder:
    """
    `Encoder` is a util class that detects faces in the image,
    extracts boxes that contain them and for every box returns
    an `<numpy.ndarray>` with the image inside the box encoded
    """

    def __init__(self, method='hog'):
        self.method = method

    def locate(self, arr):
        return face_recognition.face_locations(
            img=arr,
            model=self.method
        )

    def _encode_single(self, arr):
        boxes = self.locate(arr)
        return face_recognition.face_encodings(
            face_image=arr,
            known_face_locations=boxes
        )

    def _encode_multiple(self, list_array):
        res = []
        for arr in list_array:
            res.append(self.locate(arr))
        return res

    def encode(self, *args):

        if len(args) == 1:
            return self._encode_single(args[0])
        else:
            return self._encode_multiple(args)
