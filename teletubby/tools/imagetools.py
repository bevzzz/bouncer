import io
from mtcnn import MTCNN
from PIL import Image


def _get_binding_box(picture):
    faces = MTCNN().detect_faces(picture)
    return [f['box'] for f in faces]


def extract_resized_faces(picture):
    """
    Receives a picture as an N-dimensional array, detects a face using MTCNN()
    Crops the image and turns in into an PIL.Image object to later transform it to bytes
    Resizes it to 224x224px (this size is suitable for NNs used to perform facial recognition)
    :param picture: N-dimensional numpy array
    :return: bytes-array
    """
    binding_boxes = _get_binding_box(picture)
    extracted_faces = []
    for box in binding_boxes:
        cropped_face = _crop_image(picture, box)
        img = Image.fromarray(cropped_face)
        resized_img = _resize_to_224x224(img)
        bytes_image = _image_to_byte_array(resized_img)
        extracted_faces.append(bytes_image)
    return extracted_faces


def _crop_image(picture, box):
    x0, y0, width, height = box
    x1, y1 = x0 + width, y0 + height
    return picture[y0:y1, x0:x1]


def _resize_image_to_224x224(image, size):
    return image.resize(size)

def _resize_array_to_224x224(array, shape):
    return array.reshape(224, 224)

def resize_to_224x224(image):
    if type(image) == "Image":
        res = _resize_image_to_224x224(image, (224, 224))
    elif type(image) == "numpy_array":
        res = _resize_array_to_224x224(image, (224, 224))

def _image_to_byte_array(image: Image):
    bytes_img = io.BytesIO()
    image.save(bytes_img, format='jpeg')
    return bytes_img.getvalue()


def draw_boxes_around_faces(picture):
    """
    Returns the original picture with all detected faces outlined
    TODO: decide if a PIL.Image object or a bytes-array
    :param picture: N-dimensional array
    :return: tbd
    """
    binding_boxes = _get_binding_box(picture)
    for box in binding_boxes:
        picture = _draw_box(picture, box)
    pass


def _draw_box(picture, box):
    # TODO: DRAW A BOX AROUND THE FACE
    return picture
