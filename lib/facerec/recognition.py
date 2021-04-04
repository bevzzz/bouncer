#!/home/dmytro/pycharm/bouncer/bouncerenv/bin/python3

import base64
import collections
from lib.utils.helpers import dict_len
from flask import Flask, jsonify, request
from lib.facerec.model import Model
from lib.storage.localStorage import LocalStorage

# TODO: make environment variables in docker-compose
PICTURES_DIRECTORY = '/home/dmytro/pycharm/bouncer/new/server/pictures'

storage = LocalStorage(root_path=PICTURES_DIRECTORY)

base_url = '/bouncer/v1'
app = Flask(__name__)

encodings = storage.read_pickle('model', 'encodings.pickle')
model = Model(encodings)


def list_images_for_people(people=None):

    if people is None:
        people = get_all_people()

    if not isinstance(people, list):
        people = [people]

    personImages = collections.defaultdict()

    for person in people:
        if storage.exists_directory(person):
            personImages[person] = storage.list_directory(person)
        else:
            personImages[person] = []

    return dict(personImages)


def load_images_from_dict(imagesDict):

    for person in imagesDict.keys():

        byte_images = [storage.read_image(person, filename) for filename in imagesDict[person]]
        imagesDict[person] = byte_images

    return imagesDict


def get_all_people():
    directories = storage.list_directory()
    directories.remove("model")
    return directories


def decode_base64_string(b64):
    return base64.decodebytes(b64.encode())


def decode_hex_string(hex_str):
    return bytes.fromhex(hex_str)


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 1


@app.route(f'{base_url}/people', methods=['GET'])
def list_people():
    people = get_all_people()
    return jsonify(
        status=200,
        people=people
    )


@app.route(f'{base_url}/people/count', methods=['GET'])
def count_images_of_person(person=None):
    person_images = list_images_for_people(person)
    count = dict_len(person_images)
    status = 200

    return jsonify(
        response=dict(
            status=status,
            content=dict(
                count=count
            )
        )
    )


@app.route(f'{base_url}/model/train', methods=['POST'])
def train():

    people = request.json.get('people')
    imagesDict = list_images_for_people(people)
    train_set = load_images_from_dict(imagesDict)

    encodings_data = model.train(train_set=train_set)
    storage.write_pickle(encodings_data, 'encodings.pickle', to_dir='model')

    status = 200
    message = f'Successfully trained for {", ".join(people)}'
    image_count = dict_len(train_set)

    return jsonify(
        response=dict(
            status=status,
            content=dict(
                people=people,
                message=message,
                image_count=image_count
            )
        )
    )


@app.route(f'{base_url}/model/recognize', methods=['POST'])
def recognize():

    img = request.json.get('img')
    img = decode_base64_string(img)
    person = model.recognize(img)

    status = 200

    return jsonify(
        response=dict(
            status=status,
            content=dict(
                person=person
            )
        )
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
