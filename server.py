"""Cafe Finder Application Flask server."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ["YELP_KEY"]


@app.route("/")
def homepage():
    """Show the homepage."""

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("homepage.html")


@app.route("/login")
def login_page():
    """Show user the log in page."""
    
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Log in an existing user."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email=email)
    
    if not user:
        flash("The email you typed in does not exist. Please sign up for an account.")
        return redirect("/login")
    
    elif user.password != password:
        flash("Incorrect password. Please try again.")
        return redirect("/login")
    
    else:
        session["user_email"] = user.email
        session["user_fname"] = user.fname
        session["user_id"] = user.user_id
        return redirect("/dashboard")
    
    
@app.route("/signup")
def signup_page():
    """Show user the sign up page."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = crud.get_user_by_email(email)

    if user is not None:
        flash("An account already exists with that email. Please try another one.")
        return redirect("/signup")

    else:
        user = crud.create_user(email, password, fname, lname)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created successfully. Please log in.")
        return redirect("/login")
    
    
@app.route("/dashboard")
def dashboard():
    """Show user dashboard search form."""

    if "user_id" in session:
        return render_template("dashboard.html", name=session["user_fname"])
    return redirect("/")


@app.route("/profile/<user_id>")
def profile(user_id):
    """Show a user's profile."""

    user = crud.get_user_by_id(user_id)
    reviews = crud.get_all_user_cafe_reviews(user_id)

    return render_template("profile.html", user=user, reviews=reviews)


@app.route("/profile/<review_id>/removereview", methods=["POST"])
def remove_review(review_id):
    """Remove a user's review."""

    user = session["user_id"]
    crud.remove_review_from_db(review_id)

    flash(f"You have successfully deleted the review.")

    return redirect(f"/profile/{user}")


@app.route("/bookmarks")
def bookmarks():
    """Show a user's bookmarks."""

    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        bookmarks = crud.get_bookmarks_by_userid(session["user_id"])

        return render_template("bookmarks.html", user=user, bookmarks=bookmarks)
    return redirect("/")


@app.route("/mycafes")
def mycafes():
    """Show a user's list of already visited cafes."""

    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        visits = crud.get_visit_cafes(session["user_id"])

        return render_template("mycafes.html", user=user, visits=visits)
    return redirect("/")


@app.route("/api/mycafes")
def get_mycafes():
    """JSON information about cafes."""

    cafes = crud.get_visit_cafes(session["user_id"])
    markers = []

    for cafe in cafes:
        markers.append({
                "name": cafe.cafe.name, 
                "lat": cafe.cafe.latitude, 
                "lng": cafe.cafe.longitude,
                "address": cafe.cafe.address,
                "city": cafe.cafe.city,
                "state": cafe.cafe.state,
                "zip_code": cafe.cafe.zip_code,
                "phone": cafe.cafe.phone,
                })
       
    return jsonify(markers)


@app.route("/mycafes/<visit_id>/addnote", methods=["POST"])
def create_note(visit_id):
    """Create a note for a particular cafe."""

    user_id = session["user_id"]
    note = request.form.get("cafe-note")

    if not note:
        flash("This field cannot be blank.")
    else:
        user = crud.get_user_by_id(user_id)
        visit = crud.get_visit_by_id(visit_id)

        cafe_note = crud.create_cafe_note(user, visit, note)
        db.session.add(cafe_note)
        db.session.commit()

        flash(f"You have successfully created a note for {visit.cafe.name}.")

    return redirect("/mycafes")


@app.route("/mycafes/<note_id>/removenote", methods=["POST"])
def remove_note(note_id):
    """Remove a note from user's already visited cafes page."""

    crud.remove_note_from_db(note_id)

    return redirect("/mycafes")


@app.route("/cafe/search")
def search_cafes():
    """Search for cafes."""

    cafe = request.args.get("location")
    cafes = crud.get_cafe(cafe, cafe, cafe)

    if cafes:
        return render_template("cafe_results.html", cafes=cafes)
    else:
        flash("Sorry, we can't find a cafe with those keywords. Please try again.")
        return redirect("/dashboard")


@app.route("/cafe/<cafe_id>")
def show_cafe(cafe_id):
    """Show details of a particular cafe."""

    cafe = crud.get_cafe_by_id(cafe_id)
    reviews = crud.get_all_cafe_reviews(cafe_id) 

    all_reviews = []
    for review in reviews: 
        date_time = review.time_created.strftime("%d/%m/%y")
        all_reviews.append([review.user.fname, review.user.lname, review.user.user_id, review.review, date_time, review.rating])

    if "user_id" in session:
        bookmarked = crud.get_bookmark_by_userandcafeid(session["user_id"], cafe_id)
        visited = crud.get_cafe_visit_by_userandcafeid(session["user_id"], cafe_id)

        return render_template("cafe_details.html", cafe=cafe, reviews=all_reviews, bookmarked=bookmarked, visited=visited)

    return render_template("cafe_details.html", cafe=cafe, reviews=all_reviews)


@app.route("/cafe/<cafe_id>/review", methods=["POST"])
def create_reviews(cafe_id):
    """Create a new review for a cafe."""

    user_review = request.form.get("review")
    user_rating = request.form.get("rating")
    user = crud.get_user_by_id(session["user_id"])
    cafe = crud.get_cafe_by_id(cafe_id)
    
    review = crud.create_review(user, cafe, user_review, user_rating)
    db.session.add(review)
    db.session.commit()

    flash("You have successfully submitted a review.")

    return redirect(f"/cafe/{cafe_id}")


@app.route("/cafe/<cafe_id>/bookmark", methods=["POST"])
def bookmark_cafe(cafe_id):
    """Add a cafe to user's bookmarks."""
 
    bookmark = crud.get_bookmark_by_userandcafeid(session["user_id"], cafe_id)

    # If a user already bookmarked the cafe, this route will remove the bookmark.
    if bookmark:
        crud.remove_bookmark_from_db(session["user_id"], cafe_id)
        return "You have successfully removed a bookmark."
    # If a user hasn't bookmarked the cafe, this route will add a bookmark.
    else:
        user = crud.get_user_by_id(session["user_id"])
        cafe = crud.get_cafe_by_id(cafe_id)

        bookmark = crud.create_bookmark(user, cafe)
        db.session.add(bookmark)
        db.session.commit()
        return "You have successfully bookmarked this cafe." 


@app.route("/cafe/<cafe_id>/removebookmark", methods=["POST"])
def remove_bookmark(cafe_id):
    """Remove a cafe bookmark from user's bookmarks page."""

    # This will remove a cafe bookmark from the user's bookmarks page.
    crud.remove_bookmark_from_db(session["user_id"], cafe_id)

    return "You have successfully removed a bookmark."


@app.route("/cafe/<cafe_id>/mycafes", methods=["POST"])
def add_to_my_cafes(cafe_id):
    """Add a cafe to user's visited cafe list."""

    visit = crud.get_cafe_visit_by_userandcafeid(session["user_id"], cafe_id)

    if visit:
        crud.remove_visit_from_db(session["user_id"], cafe_id)
        return "You have successfully removed this cafe from My Cafes."
    else:
        user = crud.get_user_by_id(session["user_id"])
        cafe = crud.get_cafe_by_id(cafe_id)

        visit = crud.create_cafe_visit(user, cafe)
        db.session.add(visit)
        db.session.commit()
        return "You have successfully added this cafe to My Cafes."


@app.route("/cafe/<cafe_id>/removecafevisit", methods=["POST"])
def remove_cafevist(cafe_id):
    """Remove a visited cafe from user's cafe page."""

    crud.remove_visit_from_db(session["user_id"], cafe_id)

    return "You have successfully removed this cafe." 


@app.route("/logout")
def logout():
    """Logs a user out."""

    if "user_id" in session:
        session.clear()

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')