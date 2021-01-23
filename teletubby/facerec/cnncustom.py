from abc import ABCMeta, abstractmethod


class MetaModel(metaclass=ABCMeta):

    def __init__(self, dataset=None):
        if dataset is not None:
            self.objects = dataset.objects
            self.labels = dataset.labels
            self.obj_validation = dataset.obj_validation
            self.labels_validation = dataset.labels_validation
            self.number_labels = dataset.number_labels
            self.n_classes = dataset.n_classes
        self.init_model()

    @abstractmethod
    def init_model(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def evaluate(self):
        model = self._get_model()
        score = model.evaluate(
            self.obj_validation,
            self.labels_validation,
            verbose=0
        )
        print('%s: %.2f%%' % (model.metrics_names[1], score[1]*100))

    @abstractmethod
    def _get_model(self):
        pass

