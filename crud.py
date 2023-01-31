"""CRUD operations."""

from model import db, User, Cafe, Bookmark, Review, connect_to_db

# Create = Create new data
# Read = Retrieve data the already exits
# Update = Updating data
# Delete = Deleting data

# FUNCTIONS THAT CREATE DATA (CREATE)
def create_user(email, password, fname, lname):
    """Create and return a new user."""
    
    user = User(email=email, password=password, fname=fname, lname=lname)

    return user    


def create_cafe(name, address, city, state, zip_code, phone, img_url):
    """Create and return a cafe."""

    cafe = Cafe(name=name, 
                address=address, 
                city=city, 
                state=state, 
                zip_code=zip_code, 
                phone=phone, 
                img_url=img_url)

    return cafe


def create_review(user, cafe, review):
    """Create and return a review."""

    user_review = Review(user=user, cafe=cafe, review=review)

    return user_review


def create_bookmark(user, cafe):
    """Create and return a bookmark."""

    bookmark = Bookmark(user=user, cafe=cafe)

    return bookmark

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


def get_review_by_id(review_id):
    """Return a review by review id."""

    return Review.query.get(review_id)


def get_bookmark_by_id(bookmark_id):
    """Return a bookmark by bookmark id."""

    return Bookmark.query.get(bookmark_id)


def get_bookmark_by_userandcafeid(user_id, cafe_id):
    """Returns a bookmark for a particular cafe under a user."""

    return Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.cafe_id == cafe_id).first()


# def get_bookmarks():
#     """Returns all of a user's bookmarks."""

#     return Bookmark.query.options(db.joinedload("users")).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)