import crud as crud
from model import connect_to_db, db
import os
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, redirect, flash, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRETSCETRE"
app.jinja_env.undefined = StrictUndefined

GM_KEY = os.environ['GOOGLE_MAPS_KEY']
CLOUD_KEY = os.environ['CLOUDINARY_KEY']
CLOUD_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = os.environ['CLOUD_NAME']


@app.route('/', methods=['GET'])
def displayHomepage():
    """ Display homepage """
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def displayLogin():
    """ Display login """
    msg = ""
    return render_template('login.html', message=msg)

@app.route('/login', methods=['POST'])
def processLogin():
    """ Process login """

    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_username(username)

    if not user or (user.password_hash != password) or (user.username != username):
        flash("The username, email, or password you entered is incorrect.")
        return redirect("/login")
    
    else:
        session['username'] = user.username
        session['userId'] = user.userId

        return redirect(f"/users/{user.userId}")

# Logout

# User Dashboard
@app.route("/users/<userId>")
def showUser(userId):
    """ Show details on a particular user """

    user = crud.get_user_by_id(userId)

    return render_template("userDetails.html", user=user)




# Connect to database 
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    CORS(app)

    app.run(host="0.0.0.0")