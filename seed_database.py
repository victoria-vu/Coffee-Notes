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

# This will load data from data/cafes.json and save it to a variable
with open("data/cafes.json") as f:
    cafe_data = json.loads(f.read())

# Create cafes and store them in a list
cafes_in_db = []
for cafe in cafe_data:
    name, address, city, state, zip_code, latitude, longitude, phone, img_url = (cafe["name"], 
                                                            cafe["location"]["address1"],
                                                            cafe["location"]["city"],
                                                            cafe["location"]["state"],
                                                            cafe["location"]["zip_code"], 
                                                            cafe["coordinates"]["latitude"],
                                                            cafe["coordinates"]["longitude"],
                                                            cafe["display_phone"], 
                                                            cafe["image_url"])

    db_cafe = crud.create_cafe(name, address, city, state, zip_code, latitude, longitude, phone, img_url)

    cafes_in_db.append(db_cafe)

model.db.session.add_all(cafes_in_db)
model.db.session.commit()

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "Test"
    fname = f"User {n}"
    lname = "Test"

    user = crud.create_user(email, password, fname, lname)
    model.db.session.add(user)

model.db.session.commit()