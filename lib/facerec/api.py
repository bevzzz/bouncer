# Third-party
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
parser.add_argument(
    "file",
    location='files',
    type=FileStorage,
    required=True
)


# Create dependencies
recognizer = Recognizer()
print("WORKING")

# Define endpoint
@ns.route("/recognize")
class RecognizeEndpoint(fx.Resource):

    def get(self):
        return {"healthcheck": "I'm good"}


    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        uploaded_file = args["file"]
        img_bytes = uploaded_file.stream.read()
        person = recognizer.recognize(img_bytes)
        return person, 200
