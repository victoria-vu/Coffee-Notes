"""CRUD Operations: Functions to create, retrieve, update, or delete data from the database."""

from model import db, User, Cafe, Bookmark, Note, connect_to_db


### FUNCTIONS TO CREATE ####


def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user


def create_cafe(id, name, address, city, state, phone, latitude, longitude, img_url):
    """Create and return a cafe."""

    cafe = Cafe(cafe_id=id, name=name, address=address, city=city , state=state, phone=phone, latitude=latitude, longitude=longitude, img_url=img_url)

    return cafe


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


def get_all_user_bookmarks(user_id):
    """Returns all bookmarks for a user."""

    pass


def get_note_by_bookmark_id(bookmark_id):
    """Returns a note by bookmark id."""

    pass


if __name__ == "__main__":
    from app import app
    connect_to_db(app)