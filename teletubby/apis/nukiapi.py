from abc import ABCMeta, abstractmethod


class Lock(metaclass=ABCMeta):

    def __init(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def lock(self):
        pass


class Nuki(Lock):

    def __init__(self):
        pass

    def open(self):
        pass

    def lock(self):
        pass
