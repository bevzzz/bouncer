from flask import Flask, jsonify
from random import randint

app = Flask(__name__)


people = ["jkorbut", "mnmosine", "bevzzz"]


@app.route('/bouncer/v1/people', methods=['GET'])
def get_all():
    return jsonify(people=people)


@app.route('/bouncer/v1/people/recognize', methods=['POST'])
def recognize():
    i = randint(0, 2)
    response = {
        "person": people[i]
    }
    return jsonify(**response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
