"""CRUD operations."""

from model import db, User, Cafe, Review, Bookmark, Visit, Note, connect_to_db

# Create = Create new data
# Read = Retrieve data the already exits
# Update = Updating data
# Delete = Deleting data

# FUNCTIONS THAT CREATE DATA (CREATE)
def create_user(email, password, fname, lname):
    """Create and return a new user."""
    
    user = User(email=email, password=password, fname=fname, lname=lname)

    return user    


def create_cafe(name, address, city, state, zip_code, latitude, longitude, phone, img_url):
    """Create and return a cafe."""

    cafe = Cafe(name=name, 
                address=address, 
                city=city, 
                state=state, 
                zip_code=zip_code, 
                latitude=latitude,
                longitude=longitude,
                phone=phone, 
                img_url=img_url)

    return cafe


def create_review(user, cafe, review, rating):
    """Create and return a review."""

    user_review = Review(user=user, cafe=cafe, review=review, rating=rating)

    return user_review


def create_bookmark(user, cafe):
    """Create and return a bookmark."""

    bookmark = Bookmark(user=user, cafe=cafe)

    return bookmark


def create_cafe_visit(user, cafe):
    """Create and return a visited cafe."""

    visit = Visit(user=user, cafe=cafe)

    return visit


def create_cafe_note(user, visit, note):
    """Create and return a note for a visited cafe."""

    note = Note(user=user, visit=visit, note=note)

    return note


# FUNCTIONS THAT RETRIEVE DATA (READ)
def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user with email if it exists."""

    return User.query.filter(User.email == email).first()


def get_cafe_by_id(cafe_id):
    """Return a cafe by cafe id."""

    return Cafe.query.get(cafe_id)


def get_cafe(name, city, zip_code):
    """Return cafes by name, city, or zipcode."""

    return Cafe.query.filter((Cafe.name == name) | 
                            (Cafe.city == city) | 
                            (Cafe.zip_code == zip_code)).all()


def get_cafes():
    """Returns all cafes."""

    return Cafe.query.all()


def get_visit_cafes(user_id):
    """Returns all of user's visited cafes."""

    return Visit.query.filter(Visit.user_id == user_id).all()


def get_visit_by_id(visit_id):
    """Return a cafe visit by id."""

    return Visit.query.get(visit_id)


def get_review_by_id(review_id):
    """Return a review by review id."""

    return Review.query.get(review_id)


def get_bookmark_by_id(bookmark_id):
    """Return a bookmark by bookmark id."""

    return Bookmark.query.get(bookmark_id)


def get_bookmark_by_userandcafeid(user_id, cafe_id):
    """Returns a bookmark for a particular cafe under a user."""

    return Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.cafe_id == cafe_id).first()


def get_bookmarks_by_userid(user_id):
    """Returns all of a user's bookmarks."""

    return Bookmark.query.filter(Bookmark.user_id == user_id).all()


def get_all_cafe_reviews(cafe_id):
    """Returns all reviews of a particular cafe by most recent review."""

    return Review.query.filter(Review.cafe_id == cafe_id).order_by(Review.review_id.desc()).all()


def get_all_user_cafe_reviews(user_id):
    """Returns all user cafe reviews by user ID."""

    return Review.query.filter(Review.user_id == user_id).all()


def get_cafe_visit_by_userandcafeid(user_id, cafe_id):
    """Returns a cafe visit for particular cafe under a user."""

    return Visit.query.filter(Visit.user_id == user_id, Visit.cafe_id == cafe_id).first()


def get_note_by_noteid(note_id):
    """Returns a cafe note by id."""

    return Note.query.get(note_id)


# FUNCTIONS THAT UPDATE DATA (UPDATE)


# FUNCTIONS THAT DELETE DATA (DELETE)
def remove_bookmark_from_db(user_id, cafe_id):
    """Removes a bookmark from the datebase."""

    bookmark = get_bookmark_by_userandcafeid(user_id, cafe_id)
    db.session.delete(bookmark)
    db.session.commit()


def remove_review_from_db(review_id):
    """Removes a review from the database."""

    review = get_review_by_id(review_id)
    db.session.delete(review)
    db.session.commit()


def remove_visit_from_db(user_id, cafe_id):
    """Removes a cafe visit from the database."""

    visit = get_cafe_visit_by_userandcafeid(user_id, cafe_id)
    db.session.delete(visit)
    db.session.commit()


def remove_note_from_db(note_id):
    """Removes a note for a cafe visit from the database."""

    note = get_note_by_noteid(note_id)
    db.session.delete(note)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)