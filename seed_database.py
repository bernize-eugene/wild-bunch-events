import os 
import json
from random import choice

import crud
import model
import server

# re-create database, run dropdb and createdb
os.system("dropdb wild-bunch-events")
os.system("createdb wild-bunch-events")

# connect to database and call db.create_all()
model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()


# load user data from JSON file and save as variable
with open("data/users.json") as p:
    userData = json.loads(p.read())

# create sample of users to store in a list
usersDb = []

for user in userData:
    firstName, lastName, email, phone = (
        user['firstName'],
        user['lastName'],
        user['email'],
        user['phone']
    )

    username, profileUrl, password_hash = (
        user['username'],
        user['profileUrl'],
        user['password_hash']
    )

    city, region, country = (
        user['city'],
        user['region'],
        user['country']
    )

    userDb = crud.create_user(
        firstName, lastName, email, phone,
        username, profileUrl, password_hash,
        city, region, country
    )

    usersDb.append(userDb)

# add and commit all users to database
model.db.session.add_all(usersDb)
model.db.session.commit()



