from model import connect_to_db, db
import os
from jinja2 import StrictUndefined
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRETSCETRE"
app.jinja_env.undefined = StrictUndefined

GM_KEY = os.environ["GOOGLE_MAPS_KEY"]
CLOUD_KEY = os.environ["CLOUDINARY_KEY"]
CLOUD_SECRET = os.environ["CLOUDINARY_SECRET"]
CLOUD_NAME = os.environ["CLOUD_NAME"]


@app.route('/', methods=['GET'])
def display_homepage():
    return jsonify({"Hello": "World"})

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    CORS(app)

    app.run(host="0.0.0.0")