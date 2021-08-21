class Person:
    def __init__(self, username=None):
        self._username = username

    @property
    def username(self):
        return self._username
