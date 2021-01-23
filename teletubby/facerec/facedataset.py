from abc import ABCMeta, abstractmethod
from sklearn.model_selection import train_test_split
from random import randint
from keras import utils
from teletubby.tools.imagetools import _resize_array_to_224x224
from teletubby.tools.helpers import as_float


class Dataset(metaclass=ABCMeta):

    def __init__(self, n_classes):
        self.n_classes = n_classes
        self.objects = []
        self.labels = []
        self.obj_validation = []
        self.labels_validation = []
        self.size = 0

    def populate(self):
        self._process_data()
        self._process_label()
        self.size += 1

    @abstractmethod
    def _process_data(self):
        pass

    @abstractmethod
    def _process_label(self):
        pass

    def _populate_labels(self):
        pass

    def _populate_objects(self):
        pass


class Fotoset(Dataset):
    """
    pass it the IMG objects, have it figure out its owner etc
    """

    def __init__(self, n_classes):
        super().__init__(n_classes)

    def _process_label(self):
        # get the owner's name
        pass

    def _process_data(self):
        train_test_data = self._split_train_test()
        obj_train, obj_test, label_train, label_test = train_test_data

        obj_train = self._resiz
        pass

    def _split_train_test(self):
        return train_test_split(
            self.objects,
            self.labels,
            test_size=0.3,
            random_state=randint(1, 100)
        )
