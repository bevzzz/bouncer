if __name__ == '__main__':

    from teletubby.apis.myapi_client import Client
    from teletubby.tools.camera import Camera
    from teletubby.apis.nukiapi import Nuki

    camera = Camera()
    lock = Nuki()
    client = Client(camera=camera, lock=lock)

    client.activate()
