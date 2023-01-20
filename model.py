""" Model for Wild Bunch Events """

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """ A user """
    
    __tablename__ = "users"

    # Primary key
    userId = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    #
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    profileUrl = db.Column(db.String)

    # Password hash
    password_hash = db.Column(db.String, nullable=False)

    #
    city = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)

    # Repr string
    def __repr__(self):
        return f'<User userId={self.userId} firstName={self.firstName.title()}, lastName={self.lastName.title()}, username={self.username}>'
    
    def to_dict(self):
        return {
            "userId" : self.userId,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "profileUrl": self.profileUrl,
            "city": self.city,
            "region": self.region,
            "country": self.country
        }

""" Database connection """
# NOTE: connecting to "wild-bunch-events" database

def connect_to_db(flask_app, db_uri="postgresql:///wild-bunch-events", echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

# with app.app_contect():



if __name__ == "__main__":
    from server import app
    connect_to_db(app)