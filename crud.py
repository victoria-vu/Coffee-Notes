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


def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user with a given email."""

    return User.query.filter(User.email == email).first()


def get_cafe_by_id(cafe_id):
    """Return a cafe by cafe id."""

    pass


def get_all_user_bookmarks(user_id):
    """Returns all bookmarks for a user."""

    pass


def get_note_by_bookmark_id(bookmark_id):
    """Returns a note by bookmark id."""

    pass


if __name__ == "__main__":
    from app import app
    connect_to_db(app)