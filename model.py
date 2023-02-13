"""Models for coffee finder app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)

    reviews = db.relationship("Review", back_populates="user")
    bookmarks = db.relationship("Bookmark", back_populates="user")
    note = db.relationship("Note", back_populates="user")
    recommendation = db.relationship("Recommendation", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname}>"


class Cafe(db.Model):
    """A cafe."""

    __tablename__ = "cafes"

    cafe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id = db.Column(db.String)
     
    # Cafe details
    name = db.Column(db.String)
    address = db.Column(db.String(100))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(20))
    img_url = db.Column(db.String)

    reviews = db.relationship("Review", back_populates="cafe")
    bookmarks = db.relationship("Bookmark", back_populates="cafe")
    recommendation = db.relationship("Recommendation", back_populates="cafe")

    def __repr__(self):
        return f"<Cafe cafe_id={self.cafe_id} name={self.name}>"

    
class Review(db.Model):
    """A cafe review."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review = db.Column(db.Text)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))
    time_created = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship("User", back_populates="reviews")
    cafe = db.relationship("Cafe", back_populates="reviews")

    def __repr__(self):
        return f"<Review review_id={self.review_id} rating={self.rating} time_created={self.time_created}>"


class Bookmark(db.Model):
    """A cafe bookmark."""

    __tablename__= "bookmarks"

    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="bookmarks")
    cafe = db.relationship("Cafe", back_populates="bookmarks")
    note = db.relationship("Note", back_populates="bookmarks")

    def __repr__(self):
        return f"<Bookmark bookmark_id={self.bookmark_id} user_id={self.user_id}>"


class Note(db.Model):
    """A note about a bookmarked cafe."""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    bookmark_id = db.Column(db.Integer, db.ForeignKey("bookmarks.bookmark_id"))

    user = db.relationship("User", back_populates="note")
    bookmarks = db.relationship("Bookmark", back_populates="note")

    def __repr__(self):
        return f"<Note note_id={self.note_id} user_id={self.user_id}>"


class Recommendation(db.Model):
    """A user's cafe recommendation."""

    __tablename__ = "recommendations"

    recommendation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="recommendation")
    cafe = db.relationship("Cafe", back_populates="recommendation")

    def __repr__(self):
        return f"<Recommendation recommendation_id={self.recommendation_id} user_id={self.user_id}>"


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