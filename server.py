import crud as crud
from model import connect_to_db, db
import os
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, redirect, flash, session
from flask_cors import CORS
import cloudinary.uploader
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRETSCETRE"
app.jinja_env.undefined = StrictUndefined

GM_KEY = os.environ['GOOGLE_MAPS_KEY']
CLOUD_KEY = os.environ['CLOUDINARY_KEY']
CLOUD_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = os.environ['CLOUD_NAME']

st_lucia_tz = pytz.timezone('America/St_Lucia')
current_time = datetime.now(st_lucia_tz)
timestamp = current_time.isoformat()

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
@app.route("/logout")
def logout():
    """ Delete user session on logout """

    session.pop('username', None)
    return redirect('/')

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    # Is all required information available?
    if request.method == "POST":
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        profileFile = request.files['profileUrl']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password_hash = request.form['password']
        city = request.form['userCity']
        region = request.form['userRegion']
        country = request.form['userCountry']

        # Does the user have an account?
        user = crud.get_user_by_username(username)

        result = cloudinary.uploader.upload(profileFile, 
        api_key=CLOUD_KEY, 
        api_secret=CLOUD_SECRET, 
        cloud_name=CLOUD_NAME, timestamp=timestamp)

        profileUrl = result['secure_url']

        if user: 
            msg = 'Account already exists.'
            flash(f'{msg}')
            return redirect('/login')

        else: 
            newUser = crud.create_user(
                firstName,
                lastName,
                email, 
                phone, 
                username,
                profileUrl,
                password_hash,
                city, 
                region,
                country)
            db.session.add(newUser)
            db.session.commit()
            db.session.close()

            # where does the user go after creating an account?
            user = crud.get_user_by_username(username)
            userId = user.userId

            return redirect(f'/users/{userId}')
    return render_template("register.html", msg=msg)


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