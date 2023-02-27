"""Cafe Finder Application Flask server."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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
    elif user:
        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.")
        else:
            session["user_email"] = user.email
            session["user_fname"] = user.fname
            session["user_id"] = user.user_id
            return redirect("/dashboard")
    return redirect("/login")
    
    
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

    if user:
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
    bookmarks = crud.get_bookmarked_cafes(user_id)
    recommendation = crud.get_recommendation_by_userid(user_id)

    return render_template("profile.html", user=user, reviews=reviews, bookmarks=bookmarks, recommendation=recommendation)


@app.route("/profile/<user_id>/editinformation", methods=["POST"])
def update_information(user_id):
    """Update user account information."""

    try:
        user = crud.get_user_by_id(user_id)
        
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        about_me = request.form.get("about-me")
        email = request.form.get("email")
        new_password = request.form.get("password")

        if new_password == "":
            user_password = user.password
        else: 
            user_password=generate_password_hash(new_password, method="sha256")

        user.fname = fname
        user.lname = lname
        user.about_me = about_me
        user.email = email
        user.password = user_password
        db.session.add(user)
        db.session.commit()
        flash("You have successfully updated your information.")

    except Exception as e:
        flash("Sorry, we couldn't update your information.")
        print(e)

    return redirect(f"/profile/{user_id}")


@app.route("/profile/<user_id>/addrecommendation")
def add_recommendation(user_id):
    """Create a cafe recommendation."""

    user = crud.get_user_by_id(user_id)
    existing_recommendation = crud.get_recommendation_by_userid(user_id)

    if existing_recommendation:
        crud.remove_recommendation_from_db(existing_recommendation.recommendation_id)

    cafe_id = request.args.get("recommendation")
    cafe = crud.get_cafe_by_id(cafe_id)

    recommendation = crud.create_recommendation(user, cafe)
    db.session.add(recommendation)
    db.session.commit()

    return redirect(f"/profile/{user_id}")


@app.route("/profile/<recommendation_id>/removerecommendation", methods=["POST"])
def remove_recommendation(recommendation_id):
    """Remove a user's recommendation on profile page."""

    crud.remove_recommendation_from_db(recommendation_id)

    return "You have successfully removed the recommendation from your page."


@app.route("/profile/<review_id>/editreview", methods=["POST"])
def edit_cafe_review_profile(review_id):
    """Edit a user's review from profile page."""

    try:
        new_rating = request.form.get("edit-rating")
        new_review = request.form.get("edit-review")
        old_review = crud.get_review_by_id(review_id)
        old_review.review = new_review
        old_review.rating= int(new_rating)
        old_review.time_updated = datetime.now()
        db.session.add(old_review)
        db.session.commit()
        flash("You have successfully edited your review.")

    except Exception as e:
        flash("Sorry, we couldn't update your review.")
        print(e)

    user_id = session["user_id"]
    return redirect(f"/profile/{user_id}")


@app.route("/profile/<cafe_id>/removereview", methods=["POST"])
def remove_review(cafe_id):
    """Remove a user's review through profile page."""

    crud.remove_review_from_db(session["user_id"], cafe_id)

    return "You have successfully deleted your review."


@app.route("/mycafes")
def mycafes():
    """Show a user's list of bookmarked cafes."""

    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        bookmarks = crud.get_bookmarked_cafes(session["user_id"])

        return render_template("mycafes.html", user=user, bookmarks=bookmarks)
    return redirect("/")


@app.route("/api/mycafes")
def get_mycafes():
    """JSON information about cafes."""

    cafes = crud.get_bookmarked_cafes(session["user_id"])
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


@app.route("/mycafes/<cafe_id>/removecafebookmark", methods=["POST"])
def remove_mycafe_bookmark(cafe_id):
    """Remove a bookmarked cafe from user's bookmarks page."""

    crud.remove_bookmark_from_db(session["user_id"], cafe_id)

    return "You have successfully removed this cafe." 


@app.route("/mycafes/<bookmark_id>/addnote", methods=["POST"])
def create_note(bookmark_id):
    """Create a note for a particular cafe."""

    user_id = session["user_id"]
    note = request.form.get("add-cafe-note")

    user = crud.get_user_by_id(user_id)
    bookmark = crud.get_bookmark_by_id(bookmark_id)

    cafe_note = crud.create_cafe_note(user, bookmark, note)
    print(cafe_note)
    db.session.add(cafe_note)
    db.session.commit()

    flash(f"You have successfully created a note for {bookmark.cafe.name}.")

    return redirect("/mycafes")


@app.route("/mycafes/<note_id>/editnote", methods=["POST"])
def edit_note(note_id):
    """Edit a note for a particular cafe."""

    try:
        new_note = request.form.get("edit-note")
        old_note = crud.get_note_by_noteid(note_id)
        old_note.note = new_note
        db.session.add(old_note)
        db.session.commit()
        flash("You have successfully edited your note.")
        
    except Exception as e:
        flash("Sorry, we couldn't update your note.")
        print(e)

    return redirect("/mycafes")


@app.route("/mycafes/<note_id>/removenote", methods=["POST"])
def remove_note(note_id):
    """Remove a note from user's bookmarks page."""

    crud.remove_note_from_db(note_id)

    return "You have successfully deleted a note."


@app.route("/cafe/search")
def search_cafes():
    """Search for cafes on Yelp."""

    user_input = request.args.get("term")
    location = request.args.get("location")

    if user_input == "":
        term = "coffee shop"
    else: 
        term = user_input

    url = "https://api.yelp.com/v3/businesses/search?"

    payload = {
        "term": term,
        "location": location,
        "categories": "coffee",
        "sort_by": "best_match",
        "limit": 25,
        "unit": "miles",
        }

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
        }

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    cafe_results = []    

    if "businesses" in data:
        cafes = data["businesses"]

        for cafe in cafes:
        # Check to see if cafe already exists in the database. If it does, add it to the cafe results list.
            existing_cafe = crud.get_cafe_by_yelpid(cafe["id"])

            # If cafe does not exist in the database, create new cafe and save it to database.
            if not existing_cafe:
                id, name, address, city, state, zip_code, latitude, longitude, phone, img_url = (
                                                                    cafe["id"],
                                                                    cafe["name"], 
                                                                    cafe["location"]["address1"],
                                                                    cafe["location"]["city"],
                                                                    cafe["location"]["state"],
                                                                    cafe["location"]["zip_code"], 
                                                                    cafe["coordinates"]["latitude"],
                                                                    cafe["coordinates"]["longitude"],
                                                                    cafe["display_phone"], 
                                                                    cafe["image_url"])

                db_cafe = crud.create_cafe(id, name, address, city, state, zip_code, latitude, longitude, phone, img_url)
                db.session.add(db_cafe)
                db.session.commit()

                # Check again to see if new cafe exists in the database. If it does, add it to the list.
                new_cafe = crud.get_cafe_by_yelpid(cafe["id"])

                if new_cafe:
                    cafe_results.append(new_cafe)

            else:
                cafe_results.append(existing_cafe)

    else:
        cafes = []
        return render_template("cafe_results.html", cafes=cafes)

    return render_template("cafe_results.html", cafes=cafe_results)


@app.route("/cafe/<cafe_id>")
def show_cafe(cafe_id):
    """Show details of a particular cafe."""

    cafe = crud.get_cafe_by_id(cafe_id)
    reviews = crud.get_all_cafe_reviews(cafe_id) 

    if "user_id" in session:
        bookmarked = crud.get_cafe_bookmark_by_userandcafeid(session["user_id"], cafe_id)
        return render_template("cafe_details.html", cafe=cafe, reviews=reviews, bookmarked=bookmarked)
    return render_template("cafe_details.html", cafe=cafe, reviews=reviews)


@app.route("/cafe/<cafe_id>/review", methods=["POST"])
def create_reviews(cafe_id):
    """Create a new review for a cafe."""

    user_review = request.form.get("review")
    user_rating = request.form.get("rating")
    user = crud.get_user_by_id(session["user_id"])
    cafe = crud.get_cafe_by_id(cafe_id)

    existing_review = crud.get_cafe_review_by_userandcafeid(session["user_id"], cafe_id)

    if existing_review:
        crud.remove_review_from_db(session["user_id"], cafe_id)
    review = crud.create_review(user, cafe, user_review, user_rating)
    db.session.add(review)
    db.session.commit()

    flash("You have successfully submitted a review.")

    return redirect(f"/cafe/{cafe_id}")


@app.route("/cafe/<review_id>/editreview", methods=["POST"])
def edit_cafe_review(review_id):
    """Edit a user's review from cafe page."""

    try:
        new_rating = request.form.get("edit-rating")
        new_review = request.form.get("edit-review")
        old_review = crud.get_review_by_id(review_id)
        old_review.review = new_review
        old_review.rating= int(new_rating)
        old_review.time_updated = datetime.now()
        db.session.add(old_review)
        db.session.commit()
        flash("You have successfully edited your review.")

    except Exception as e:
        flash("Sorry, we couldn't update your review.")
        print(e)

    review = crud.get_review_by_id(review_id)
    return redirect(f"/cafe/{review.cafe.cafe_id}")


@app.route("/cafe/<cafe_id>/removereview", methods=["POST"])
def remove_cafe_review(cafe_id):
    """Remove a user's review from a cafe page."""

    crud.remove_review_from_db(session["user_id"], cafe_id)

    return "You have successfully deleted your review."


@app.route("/cafe/<cafe_id>/mycafes", methods=["POST"])
def add_to_my_cafes(cafe_id):
    """Add a cafe to user's bookmark list."""

    bookmark = crud.get_cafe_bookmark_by_userandcafeid(session["user_id"], cafe_id)

    if bookmark:
        crud.remove_bookmark_from_db(session["user_id"], cafe_id)
        return "You have successfully removed this cafe from My Cafes."
    else:
        user = crud.get_user_by_id(session["user_id"])
        cafe = crud.get_cafe_by_id(cafe_id)

        bookmark = crud.create_cafe_bookmark(user, cafe)
        db.session.add(bookmark)
        db.session.commit()
        return "You have successfully added this cafe to My Cafes."


@app.route("/cafe/<cafe_id>/removecafebookmark", methods=["POST"])
def remove_cafe_bookmark(cafe_id):
    """Remove a bookmarked cafe from a cafe page."""

    crud.remove_bookmark_from_db(session["user_id"], cafe_id)

    return "You have successfully removed this cafe." 


@app.route("/logout")
def logout():
    """Logs a user out."""

    if "user_id" in session:
        session.clear()
        flash("You have signed out.")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')