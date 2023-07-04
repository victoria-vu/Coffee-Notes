"""CRUD Operations: Functions to create, retrieve, update, or delete data from the database."""

from model import db, User, Cafe, Bookmark, Note, connect_to_db


### FUNCTIONS TO CREATE ####


def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user


def create_cafe(name, address, phone, latitude, longitude, img_url):
    """Create and return a cafe."""

    cafe = Cafe(name=name, address=address, phone=phone, latitude=latitude, longitude=longitude, img_url=img_url)

    return cafe


def create_bookmark(user, cafe): 
    """Create and return a bookmark."""

    bookmark = Bookmark(user=user, cafe=cafe)

    return bookmark


def create_note(user, bookmark, note):
    """Create and return a note for a bookmark."""

    note = Note(user=user, bookmark=bookmark, note=note)

    return note


### FUNCTIONS TO RETRIEVE ###


if __name__ == "__main__":
    from app import app
    connect_to_db(app)