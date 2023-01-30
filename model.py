"""Models for coffee finder app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="user")
    bookmark = db.relationship("Bookmark", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname}>"


class Cafe(db.Model):
    """A cafe."""

    __tablename__ = "cafes"

    cafe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    # Cafe details
    name = db.Column(db.String)
    address = db.Column(db.String(100))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    img_url = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="cafe")
    bookmark = db.relationship("Bookmark", back_populates="cafe")

    def __repr__(self):
        return f"<Cafe cafe_id={self.cafe_id} name={self.name}>"

    
class Rating(db.Model):
    """A cafe rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="ratings")
    cafe = db.relationship("Cafe", back_populates="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"


class Bookmark(db.Model):
    """A cafe bookmark."""

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="bookmark")
    cafe = db.relationship("Cafe", back_populates="bookmark")

    def __repr__(self):
        return f"<Bookmark bookmark_id={self.bookmark_id}"
    

def connect_to_db(flask_app, db_uri="postgresql:///cafes", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    app.app_context().push()
    db.create_all()