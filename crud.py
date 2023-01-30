"""CRUD operations."""

from model import db, User, Cafe, Bookmark, Rating, connect_to_db

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


def get_cafe_by_name(name):
    """Return cafe by name."""

    return Cafe.query.filter(Cafe.name == name).all()


def get_cafe_by_city(city):
    """Return cafe by city."""

    return Cafe.query.filter(Cafe.city == city).all()


def get_cafe_by_zipcode(zipcode):
    """Return cafe by zipcode."""

    return Cafe.query.filter(Cafe.zipcode == zipcode).all()


def get_bookmark_by_id(bookmark_id):
    """Return a bookmark by bookmark id."""

    return Bookmark.query.get(bookmark_id)

def get_rating_by_id(rating_id):
    """Return a rating by rating id."""

    return Rating.query.get(rating_id)


def get_cafes():
    """Returns all cafes."""

    return Cafe.query.all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)