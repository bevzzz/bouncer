import io
from PIL import Image
from mtcnn import MTCNN
from matplotlib import pyplot


class FaceDetector:

    def __init__(self, picture):
        self.picture = picture
        self.detector = MTCNN()

    def extract_resized_faces(self):
        faces = self.detector.detect_faces(self.picture)
        detected_faces = []
        for f in faces:
            box = self._get_binding_box(f)
            cropped_face = self._crop_image(box)
            image_object = self._get_image_from_ndarray(cropped_face)
            resized_face = self._resize_to_224x224(image_object)
            detected_faces.append(resized_face)
        return detected_faces

    @staticmethod
    def _get_binding_box(_face):
        return _face['box']

    def _crop_image(self, box):
        x0, y0, width, height = box
        x1, y1 = x0 + width, y0 + height
        return self.picture[y0:y1, x0:x1]

    @staticmethod
    def _resize_to_224x224(image):
        image = image.resize((224, 224))
        return FaceDetector.image_to_byte_array(image)

    @staticmethod
    def _get_image_from_ndarray(ndarray_image):
        return Image.fromarray(ndarray_image)

    @staticmethod
    def image_to_byte_array(image: Image):
        bytes_img = io.BytesIO()
        image.save(bytes_img, format='jpeg')
        return bytes_img.getvalue()

    @staticmethod
    def show_image(img):
        pyplot.imshow(img)


