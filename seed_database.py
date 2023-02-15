"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb cafes")
os.system("createdb cafes")

# Need to go through model to access the database, then create all tables
model.connect_to_db(server.app)
model.db.create_all()

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "Test"
    fname = f"User {n}"
    lname = "Test"

    user = crud.create_user(email, password, fname, lname)
    model.db.session.add(user)

model.db.session.commit()