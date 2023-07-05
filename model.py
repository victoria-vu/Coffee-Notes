"""Models for Coffee Notes app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)

    bookmarks = db.relationship("Bookmark", back_populates="user")
    notes = db.relationship("Note", back_populates="user")

    def __repr__(self):
        """Return user id, name, and email of a User object."""

        return f"<User user_id={self.user_id} name={self.fname} email={self.email}>"


class Cafe(db.Model):
    """A cafe."""

    __tablename__ = "cafes"

    cafe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String, nullable=True)

    bookmarks = db.relationship("Bookmark", back_populates="cafe")

    def __repr__(self):
        """Return cafe id and name of a Cafe object."""

        return f"<Cafe cafe_id={self.cafe_id} name={self.name}>"
    

class Bookmark(db.Model):
    """A cafe bookmark."""

    __tablename__ = "bookmarks"
    __table_args__ = (db.UniqueConstraint("user_id", "cafe_id"),)

    bookmark_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.cafe_id"), nullable=False)

    user = db.relationship("User", back_populates="bookmarks")
    cafe = db.relationship("Cafe", back_populates="bookmarks")
    note = db.relationship("Note", back_populates="bookmark")

    def __repr__(self):
        """Return bookmark id and user id of a Bookmark object."""

        return f"<Bookmark bookmark_id={self.bookmark_id} user_id={self.user_id}>"
    

class Note(db.Model):
    """A note for a bookmarked cafe by a user."""

    __tablename__ = "notes"
    __table_args__ = (db.UniqueConstraint("user_id", "bookmark_id"),)

    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    bookmark_id = db.Column(db.Integer, db.ForeignKey("bookmarks.bookmark_id"), nullable=False)
    note = db.Column(db.Text, nullable=False)

    user = db.relationship("User", back_populates="notes")
    bookmark = db.relationship("Bookmark", back_populates="note")

    def __repr__(self):
        """Return note id and user id of a Note object."""

        return f"<Note note_id={self.note_id} user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///cafes_db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from app import app
    connect_to_db(app)