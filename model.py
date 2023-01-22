""" Model for Wild Bunch Events """
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

db = SQLAlchemy()

os.system("dropdb wild-bunch-events")
os.system("createdb wild-bunch-events")

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

class Event(db.Model):
    """ An event """

    __tablename__ = "events"

    # Primary Key
    eventId = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #
    name = db.Column(db.String)
    startDatetime = db.Column(db.DateTime(timezone=True))
    endDatetime = db.Column(db.DateTime(timezone=True))
    description = db.Column(db.Text)
    eventUrl =  db.Column(db.String)

    #
    city = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)

    #
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))

    def __repr__(self):
        return (
            f'<Event eventId={self.eventId} name = {self.name}>'
            f'<User userId={self.userId} eventId= {self.eventId}>'
        )

    def to_dict(self):
        return {
            "eventId" : self.eventId,
            "name" : self.name,
            "startDatetime": self.startDatetime,
            "endDatetime": self.endDatetime,
            "description" : self.description,
            "eventUrl": self.eventUrl,
            "city": self.city,
            "region" : self.region,
            "country" : self.country,
            "userId" : self.userId,
            "user" : f'{self.user.firstName.title()} {self.user.lastName.title()}'
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




if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    app.app_context().push()
    db.create_all()