""" CRUD operations -- Create Read Update Delete """

from model import db, User, Event, connect_to_db
from datetime import datetime

############### CREATION ################################

def create_user(firstName, lastName, email, phone, username, profileUrl, password_hash, city, region, country):
    """Create and return a new user"""

    user = User(
        firstName=firstName,
        lastName=lastName,
        email=email,
        phone=phone,
        username=username,
        profileUrl=profileUrl,
        password_hash=password_hash,
        city=city,
        region=region,
        country=country
    )

    return user

def create_event(name, startDatetime, endDatetime, description, category, eventUrl, city, region, country):
    """ Create and return a new event"""

    event = Event(
        name=name,
        startDatetime=startDatetime,
        endDatetime=endDatetime,
        description=description,
        category=category,
        eventUrl=eventUrl,
        city=city,
        region=region,
        country=country
    )

    return event

#################### ACCESS ###########################

def get_event_by_id(eventId):
    """ Return an event by id """

    return Event.query.get(event_id)

def get_user_by_id(userId):
    """ Return a user by id """

    return User.query.get(userId)


################# CONNECTION #############################

def connect_user_event(userId, eventId):
    """ Connect user to event and return event """

    event = get_event_by_id(eventId)
    event.userId = userId

    return event


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    app.app_context().push()
    db.create_all()