from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

ns = api.namespace("facerec", description="Recognizing people's faces")

model = api.model("recognize", {
    'name': fields.String
})


@ns.route('/recognize')
class RecognizeFace(Resource):
    def get(self):
        return "Dima"

    def post(self):
        return "Vasya"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
