"""Script to seed database."""

import os
import json

import crud
import model
import app

os.system("dropdb cafes_db")
os.system("createdb cafes_db")

model.connect_to_db(app.app)
model.db.create_all()

# Load cafe data from JSON file
with open("data/cafes.json") as f:
    cafe_data = json.loads(f.read())

# Create cafes and store them in a list
cafes_in_db = []
for cafe in cafe_data:
    name, address, city, state, phone, latitude, longitude, img_url = (
    cafe["name"], 
    cafe["location"]["display_address"][0] + " " + cafe["location"]["display_address"][1],
    cafe["location"]["city"],
    cafe["location"]["state"],
    cafe["display_phone"], 
    cafe["coordinates"]["latitude"], 
    cafe["coordinates"]["longitude"], 
    cafe["image_url"])

    db_cafe = crud.create_cafe(name, address, city, state, phone, latitude, longitude, img_url)
    cafes_in_db.append(db_cafe)

model.db.session.add_all(cafes_in_db)
model.db.session.commit()

user = crud.create_user("janedoe123@gmail.com", "janedoe123", "Jane", "Doe")
model.db.session.add(user)
model.db.session.commit()