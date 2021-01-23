# Server-side API, that communicates with Client and
# makes calls for Dvoretski functions etc.
# Sends commands to the Client such as to
# open/lock the door, take another picture etc.


class Server:

    def __init__(self, manager):
        self.manager = manager

    def activate(self):
        pass

