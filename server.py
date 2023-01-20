from model import connect_to_db, db, db_drop_and_create_all
import os
from jinja2 import StrictUndefined
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRETSCETRE"
app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=['GET'])
def display_homepage():
    return jsonify({"Hello": "World"})

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    CORS(app)
    db_drop_and_create_all(app)

    app.run(host="0.0.0.0")