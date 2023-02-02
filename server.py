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

    return render_template("dashboard.html", name=session["user_fname"])


@app.route("/profile")
def profile():
    """Show a user's profile."""

    logged_in_user = session["user_id"]
    user = crud.get_user_by_id(logged_in_user)

    return render_template("profile.html", user=user)


@app.route("/bookmarks")
def bookmarks():
    """Show a user's bookmarks."""

    logged_in_user = session["user_id"]
    user = crud.get_user_by_id(logged_in_user)
    bookmarks = crud.get_bookmarks_by_userid(logged_in_user)

    return render_template("bookmarks.html", user=user, bookmarks=bookmarks)


@app.route("/mycafes")
def mycafes():
    """Show a user's list of already visited cafes."""

    logged_in_user = session["user_id"]
    user = crud.get_user_by_id(logged_in_user)
    visits = crud.get_visit_cafes(logged_in_user)

    return render_template("mycafes.html", user=user, visits=visits)


@app.route("/cafe/search", methods=["POST"])
def search_cafes():
    """Search for cafes."""

    cafe = request.form.get("location")
    cafes = crud.get_cafe(cafe, cafe, cafe)

    if cafes:
        return render_template("cafe_results.html", cafes=cafes)
    else:
        flash("Sorry, we can't find a cafe with those keywords. Try again")
        return redirect("/dashboard")


@app.route("/cafe/<cafe_id>")
def show_cafe(cafe_id):
    """Show details of a particular cafe."""

    logged_in_user = session["user_id"]
    cafe = crud.get_cafe_by_id(cafe_id)
    reviews = crud.get_all_cafe_reviews(cafe_id)
    bookmarked = crud.get_bookmark_by_userandcafeid(logged_in_user, cafe_id)
    visited = crud.get_cafe_visit_by_userandcafeid(logged_in_user, cafe_id)

    if bookmarked or visited:
        return render_template("cafe_details.html", cafe=cafe, reviews=reviews, bookmarked=bookmarked, visited=visited)

    return render_template("cafe_details.html", cafe=cafe, reviews=reviews, bookmarked=bookmarked, visited=visited)


@app.route("/cafe/<cafe_id>/review", methods=["POST"])
def create_reviews(cafe_id):
    """Create a new rating for a cafe."""

    user_id = session["user_id"]
    user_review = request.form.get("review")

    if user_id is None:
        flash("You must log in to review a cafe.")
    elif not user_review:
        flash("This field cannot be blank.")
    else:
        user = crud.get_user_by_id(user_id)
        cafe = crud.get_cafe_by_id(cafe_id)

        review = crud.create_review(user, cafe, str(user_review))
        db.session.add(review)
        db.session.commit()

        flash("You have successfully submitted a review.")

    return redirect(f"/cafe/{cafe_id}")


@app.route("/cafe/<cafe_id>/bookmark", methods=["POST"])
def bookmark_cafe(cafe_id):
    """Add cafe to user's bookmarks."""
 
    user_id = session["user_id"]
    bookmark = crud.get_bookmark_by_userandcafeid(user_id, cafe_id)

    if user_id is None:
        flash("You must log in to bookmark this cafe.")
    elif bookmark:
        crud.remove_bookmark_from_db(user_id, cafe_id)
        # return "You already bookmarked this cafe!"
        return "You have successfully removed a bookmark."
    else:
        user = crud.get_user_by_id(user_id)
        cafe = crud.get_cafe_by_id(cafe_id)

        bookmark = crud.create_bookmark(user, cafe)
        db.session.add(bookmark)
        db.session.commit()

        return "You have successfully bookmarked this cafe." 


@app.route("/cafe/<cafe_id>/removebookmark", methods=["POST"])
def remove_bookmark(cafe_id):
    """Remove cafe from user's bookmarks."""

    user_id = session["user_id"]
    crud.remove_bookmark_from_db(user_id, cafe_id)

    return "You have successfully removed a bookmark."


@app.route("/cafe/<cafe_id>/mycafes", methods=["POST"])
def add_to_my_cafes(cafe_id):
    """Add cafe to user's visited cafe list."""

    user_id = session["user_id"]
    visit = crud.get_cafe_visit_by_userandcafeid(user_id, cafe_id)

    if user_id is None:
        flash("You must log in to add this cafe.")
    elif visit:
        crud.remove_visit_from_db(user_id, cafe_id)
        return "You have successfully removed this cafe from My Cafes."
    else:
        user = crud.get_user_by_id(user_id)
        cafe = crud.get_cafe_by_id(cafe_id)

        visit = crud.create_cafe_visit(user, cafe)
        db.session.add(visit)
        db.session.commit()
        return "You have successfully added this cafe to My Cafes."


@app.route("/cafe/<cafe_id>/removecafevisit", methods=["POST"])
def remove_cafevist(cafe_id):
    """Remove a visited cafe from user's cafe page."""

    user_id = session["user_id"]
    crud.remove_visit_from_db(user_id, cafe_id)

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