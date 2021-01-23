import os
import skimage.io as io
import numpy as np
from sklearn.model_selection import train_test_split
from random import randint
from abc import ABCMeta, abstractmethod
from keras import utils


class FaceDataSet(metaclass=ABCMeta):

    def __init__(self, path, extension_list, n_classes):
        self.path = path  # folder containing the images
        self.extension_list = extension_list  # extensions of the files to look for, like .jpeg
        self.n_classes = n_classes  # number ob classes to categorize into
        self.objects = []  # images to use for CNN training
        self.labels = []  # labels for categories
        self.obj_validation = []  # validation sample
        self.labels_validation = []  # labels for the validation sample
        self.number_labels = 0  # total number of labels in the dataset (not like the size of the dataset?)

    def _get_data(self):
        img_path_list = os.listdir(self.path)
        self.objects, self.labels = self.fetch_img_path(img_path_list, self.path, vgg_img_processing)
        self._process_data(vgg_img_processing)

    @abstractmethod
    def _process_data(self, img_processing):
        pass

    def fetch_img_path(self, img_path_list, path, vgg_img_processing):
        images = []
        labels = []
        for img_path in img_path_list:
            if self._check_ext(img_path):
                img_abs_path = os.path.abspath(os.path.join(path, img_path))
                image = io.imread(img_abs_path, as_gray=True)
                label = self._process_label(img_path)
                images.append(image)
                labels.append(label)
        return images, labels

    def _check_ext(self, img_path):
        return any(img_path.endswith(ext) for ext in self.extension_list)

    @abstractmethod
    def _process_label(self, img_path):
        pass


class YaleFaceDataset(FaceDataSet):

    def __init__(self, path, extension_list, n_classes):
        super().__init__(path, extension_list, n_classes)

    def _process_label(self, img_path):
        val = int(os.path.split(img_path)[1].split(".")[0].replace("subject", "")) - 1
        if val not in self.labels:
            self.number_labels += 1
        return val

    def _process_data(self, img_processing):
        train_test_out = self._split_training_set()
        self.objects, self.obj_validation, self.labels, self.labels_validation = train_test_out

        self.labels = utils.to_categorical(self.labels, self.n_classes)
        self.labels_validation = utils.to_categorical(self.labels, self.n_classes)

        self.object = Utils.reshape_rescale_data(self.objects)
        self.obj_validation = Utils.reshape_rescale_data(self.obj_validation)

    def _split_training_set(self):
        test_split = train_test_split(
            self.objects,
            self.labels,
            test_size=0.3,
            random_state=randint(0, 100)
        )
        return test_split


class Utils:

    @staticmethod
    def reshape_rescale_data(data):
        data = np.array(data)
        res = data.reshape(224, 224)  # for grayscale images 3rd argument is 1
        return Utils.as_float(res)

    @staticmethod
    def as_float(value):
        return value.astype('float32')/255

