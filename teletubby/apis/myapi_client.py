"""
Client-side API. Communicates with the Server and
makes calls for Lock's and Camera's function
"""


class Client:

    def __init__(self, camera, lock):
        self.camera = camera
        self.lock = lock

    def activate(self):
        pass
