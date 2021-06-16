import numpy as np
import cv2 as cv
import time
import requests
import base64
from lib.camera.drawer import add_stuff


def recognize(img):
    base_url = 'http://localhost:5000/bouncer/v1/model/recognize'
    img = img.tobytes()
    img = base64.encodebytes(img).decode('utf-8')

    body_json = {
        'img': img
    }

    response = requests.post(url=base_url, json=body_json).json()

    if response['content']['status'] == 200:
        return response['content']['person']
    else:
        return 'Unknown'


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    name = recognize(frame)
    frame = add_stuff(frame, name)

    # Display the resulting frame
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()