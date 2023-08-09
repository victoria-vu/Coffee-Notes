"""CRUD Operations: Functions to create, retrieve, update, or delete data from the database."""

from model import db, User, Cafe, BusinessHours, Bookmark, Note, connect_to_db
from werkzeug.security import generate_password_hash
from flask import flash
from datetime import datetime
import calendar


### FUNCTIONS TO CREATE ####


def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(
        email=email, 
        password=generate_password_hash(password, method="scrypt"), 
        fname=fname, 
        lname=lname
    )

    return user


def create_cafe(id, name, address, city, state, phone, latitude, longitude, img_url):
    """Create and return a cafe."""

    cafe = Cafe(
        cafe_id=id, 
        name=name, 
        address=address, 
        city=city , 
        state=state, 
        phone=phone, 
        latitude=latitude, 
        longitude=longitude, 
        img_url=img_url
    )

    return cafe


def create_businesshours(day, hours, cafe):
    """Create and return a business hour."""

    business_hour = BusinessHours(day=day, hours=hours, cafe_id=cafe)

    return business_hour


def create_bookmark(user, cafe): 
    """Create and return a bookmark."""

    bookmark = Bookmark(user_id=user, cafe_id=cafe)

    return bookmark


def create_note(user, bookmark, note):
    """Create and return a note for a bookmark."""

    note = Note(user_id=user, bookmark_id=bookmark, note=note)

    return note


### FUNCTIONS TO RETRIEVE ###


def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user with a given email."""

    return User.query.filter(User.email == email).first()


def get_cafe_by_id(cafe_id):
    """Return a cafe by cafe id."""

    return Cafe.query.get(cafe_id)


def get_cafe_by_bookmark_id(bookmark_id):
    """Return a cafe by bookmark id."""

    bookmark = Bookmark.query.filter(Bookmark.bookmark_id == bookmark_id).first()

    return bookmark.cafe


def get_business_hours_by_cafe_id(cafe_id):
    """Return cafe business hours dictionary by cafe id."""

    cafe_hours = {}

    business_hours = BusinessHours.query.filter_by(cafe_id = cafe_id).all()
    
    for business_hour in business_hours:
        if business_hour.hours != "Closed":
            military_times = business_hour.hours.split("-")
            standard_times = []
            for time in military_times:
                dt = datetime.strptime(time, "%H%M")
                standard_time = dt.strftime("%I:%M%p")
                standard_times.append(standard_time.lstrip("0"))
            cafe_hours[calendar.day_abbr[business_hour.day]] = f"{standard_times[0]}-{standard_times[1]}"
        else: 
            cafe_hours[calendar.day_abbr[business_hour.day]] = business_hour.hours

    return cafe_hours


def get_all_user_bookmarks(user_id):
    """Return all bookmarks for a user by user id."""

    return Bookmark.query.filter(Bookmark.user_id == user_id).all()


def get_bookmark_by_user_and_cafe_id(user_id, cafe_id):
    """Return a bookmark for a user by user and cafe id."""

    return Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.cafe_id == cafe_id).first()


def get_note_by_bookmark_id(bookmark_id):
    """Return a note by bookmark id."""

    return Note.query.filter(Note.bookmark_id == bookmark_id).first()


### FUNCTIONS TO UPDATE ###


def update_note(existing_note, new_note):
    """Update an existing note."""

    try:
        existing_note.note = new_note
        db.session.add(existing_note)
        db.session.commit()
    except Exception as e:
        flash("Sorry, we couldn't update your note.")
        print(e)


### FUNCTIONS TO DELETE ###


def delete_note(existing_note):
    """Delete an existing note."""

    db.session.delete(existing_note)
    db.session.commit()


if __name__ == "__main__":
    from app import app
    connect_to_db(app)