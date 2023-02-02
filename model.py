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

    reviews = db.relationship("Review", back_populates="user")
    bookmark = db.relationship("Bookmark", back_populates="user")
    visit = db.relationship("Visit", back_populates="user")
    note = db.relationship("Note", back_populates="user")

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

    reviews = db.relationship("Review", back_populates="cafe")
    bookmark = db.relationship("Bookmark", back_populates="cafe")
    visit = db.relationship("Visit", back_populates="cafe")

    def __repr__(self):
        return f"<Cafe cafe_id={self.cafe_id} name={self.name}>"

    
class Review(db.Model):
    """A cafe review."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="reviews")
    cafe = db.relationship("Cafe", back_populates="reviews")

    def __repr__(self):
        return f"<Review review_id={self.review_id}>"


class Bookmark(db.Model):
    """A cafe bookmark."""

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="bookmark")
    cafe = db.relationship("Cafe", back_populates="bookmark")

    def __repr__(self):
        return f"<Bookmark bookmark_id={self.bookmark_id}>"


class Visit(db.Model):
    """A visited cafe."""

    __tablename__= "visits"

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"))

    user = db.relationship("User", back_populates="visit")
    cafe = db.relationship("Cafe", back_populates="visit")
    note = db.relationship("Note", back_populates="visit")


class Note(db.Model):
    """A note about a visited cafe."""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.user_id"))

    user = db.relationship("User", back_populates="note")
    visit = db.relationship("Visit", back_populates="note")


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