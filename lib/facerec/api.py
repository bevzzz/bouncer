# Build-in libraries
import os
import pickle

# Third-party libraries
import flask as f
import flask_restx as fx
from werkzeug.datastructures import FileStorage

# Local libraries
from lib.facerec.recognize import Recognizer

# Define the RestX API instance
app = f.Flask(__name__)
api = fx.Api(
    app=app,
    version="1.0",
    title="Facerec",
    description="Recognize faces"
)

# Define namespaces for the API
ns = api.namespace("facerec")


# Set up request parsing
parser = fx.reqparse.RequestParser()

# Define a parser for the Recognize endpoint
recognize_parser = parser.copy()
recognize_parser.add_argument(
    "file",
    location='files',
    type=FileStorage,
    required=True
)

# Define response model
recognize_response = ns.model(
    "Recognition", {
        "username": fx.fields.String
    }
)

# Define parser for Train endpoint
train_parser = parser.copy()
train_parser.add_argument("for_names", location="json", type=list)
train_parser.add_argument("save_new", location="json", type=fx.inputs.boolean)
train_parser.add_argument("set_new", location="json", type=fx.inputs.boolean)


# Create dependencies
encodings_path = "/home/dmytro/pycharm/bouncer/resources/model/encodings.pickle"
if os.path.exists(encodings_path):
    with open(encodings_path, "rb") as rb:
        known_encodings = pickle.load(rb)
else:
    known_encodings = None
recognizer = Recognizer(known=known_encodings)


# Define endpoint
@ns.route("/recognize")
class RecognizeEndpoint(fx.Resource):

    def get(self):
        return {"healthcheck": "I'm good"}

    @ns.expect(recognize_parser)
    @ns.marshal_with(recognize_response)
    def post(self):
        args = recognize_parser.parse_args()
        uploaded_file = args["file"]
        img_bytes = uploaded_file.stream.read()
        person = recognizer.recognize(img_bytes)
        return person, 200


@ns.route("/train")
class TrainEndpoint(fx.Resource):

    @ns.expect(train_parser)
    def post(self):
        args = train_parser.parse_args()
        ok = recognizer.train(
            names=args["for_names"],
            save_new=args["save_new"],
            set_new=args["set_new"]
        )
        return ok, 200
