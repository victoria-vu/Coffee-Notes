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

# Create cafes and business hours for database
for cafe in cafe_data:
    id, name, address, city, state, phone, latitude, longitude, img_url = (
    cafe["id"],
    cafe["name"], 
    cafe["location"]["display_address"][0] + " " + cafe["location"]["display_address"][1],
    cafe["location"]["city"],
    cafe["location"]["state"],
    cafe["display_phone"], 
    cafe["coordinates"]["latitude"], 
    cafe["coordinates"]["longitude"], 
    cafe["image_url"]
    )

    db_cafe = crud.create_cafe(id, name, address, city, state, phone, latitude, longitude, img_url)
    model.db.session.add(db_cafe)
    model.db.session.commit()

    # Adds business hours for the cafe
    hours = cafe["hours"][0]["open"]
    business_hours = {}

    for day_num in range(0, 7):
        day_data = next((item for item in hours if item["day"]== day_num), None)
        if day_data is None:
            business_hours[day_num] = "Closed"
        else:
            start_time = day_data["start"]
            end_time = day_data["end"]
            business_hours[day_num] = f"{start_time}-{end_time}"

    for day, hours in business_hours.items():
        business_hour = crud.create_businesshours(day, hours, id)
        model.db.session.add(business_hour)
        model.db.session.commit()

# Create a fake user
user = crud.create_user("janedoe@gmail.com", "janedoe", "Jane", "Doe")
model.db.session.add(user)
model.db.session.commit()