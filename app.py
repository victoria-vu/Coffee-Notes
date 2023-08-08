"""Server for Coffee Notes app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
import requests
import os


app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ["YELP_KEY"]


### ROUTES FOR HOMEPAGE AND LOGIN ###
@app.route("/")
def homepage(): 
    """View homepage."""

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("homepage.html")


@app.route("/signup")
def signup_page():
    """View sign up page."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    existing_user = crud.get_user_by_email(email)

    if existing_user:
        flash("An account already exists with that email. Please try another one.")
        return redirect("/signup")
    else:
        user = crud.create_user(email, password, fname, lname)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created successfully. Please log in.")
        return redirect("/login")


@app.route("/login")
def login_page():
    """View log in page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():
    """Log in an existing user."""

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if not user:
        flash("The email you typed in does not exist. Please sign up for an account or try again.")
    elif user:
        if password != password:
            flash("Incorrect password. Please try again.")
        else:
            session["user_id"] = user.user_id
            session["name"]= user.fname
            session["email"] = user.email
            flash("Logged in successfully.")
            return redirect("/dashboard")
    return redirect("/login")


@app.route("/logout")
def logout_user():
    """Log a user out of the session."""

    if "user_id" in session:
        session.clear()
        flash("You have signed out.")

    return redirect("/")


### ROUTES FOR USER DASHBOARD AND PROFILE ###
@app.route("/dashboard")
def dashboard_page():
    """View user dashboard and search form."""

    if "user_id" in session:
        return render_template("dashboard.html", name=session["name"])
    return redirect("/")


@app.route("/profile/<user_id>")
def profile_page(user_id):
    """View user profile page."""

    user = crud.get_user_by_id(user_id)
    bookmarks = user.bookmarks

    return render_template("profile.html", user=user, bookmarks=bookmarks)


### ROUTES FOR CAFE SEARCH/DETAILS ###
@app.route("/cafe/search")
def search_cafes():
    """Search for cafes via Yelp API."""

    term = request.args.get("term", "coffee shop")
    location = request.args.get("location")

    url = "https://api.yelp.com/v3/businesses/search"
    payload = {
        "term": term,
        "location": location,
        "radius": 40000,
        "categories": "coffee",
        "limit": 50
    }
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    res = requests.get(url, params=payload, headers=headers)
    data = res.json()

    if "businesses" in data:
        cafes = data["businesses"]
        total = len(data["businesses"])
        return render_template("search_results.html", term=term, total=total, results=cafes)
    else:
        flash("Sorry, but nothing matched your search criteria. Please try again.")
        return redirect("/dashboard")


@app.route("/cafe/<id>")
def cafe_page(id):
    """View details of a cafe."""

    url = f"https://api.yelp.com/v3/businesses/{id}"
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    cafe_in_db = crud.get_cafe_by_id(id)

    # Creates a cafe object to add into database
    if not cafe_in_db:
        new_cafe = crud.create_cafe(id,
                    data["name"], 
                    data["location"]["address1"] + ", " + data["location"]["city"] + ", " + data["location"]["state"] + " " + data["location"]["zip_code"],
                    data["location"]["city"],
                    data["location"]["state"],
                    data["display_phone"], 
                    data["coordinates"]["latitude"], 
                    data["coordinates"]["longitude"], 
                    data["image_url"]
                    )
        
        db.session.add(new_cafe)
        db.session.commit()

        # Adds business hours for the cafe
        hours = data["hours"][0]["open"]
        business_hours = {}

        for day_num in range(0, 7):
            day_data = next((item for item in hours if item["day"]== day_num), None)
            if day_data is None:
                business_hours[day_num] = "Closed"
            else:
                start_time = day_data["start"]
                end_time = day_data["end"]
                business_hours[day_num] = f"{start_time}-{end_time}"

        for day, hours in business_hours.items():
            business_hour = crud.create_businesshours(day, hours, id)
            db.session.add(business_hour)
            db.session.commit()
            print("Successfully added business hours")

    cafe = crud.get_cafe_by_id(id)
    cafe_hours = crud.get_business_hours_by_cafe_id(id)
    user_id = session["user_id"]
    bookmarked = crud.get_bookmark_by_user_and_cafe_id(user_id, id)

    return render_template("cafe_details.html", cafe=cafe, cafe_hours=cafe_hours, bookmarked=bookmarked)


### ROUTES FOR BOOKMARKS ###
@app.route("/bookmark", methods=["POST"])
def add_bookmark():
    """Create a bookmark."""

    user_id = session["user_id"]
    cafe_id = request.form.get("cafe-id")
    cafe = crud.get_cafe_by_id(cafe_id)

    bookmark = crud.create_bookmark(user_id, cafe_id)
    db.session.add(bookmark)
    db.session.commit()

    flash(f"You have successfully added {cafe.name} to My Bookmarks.")
    return redirect(f"/cafe/{cafe_id}")


@app.route("/removebookmark", methods=["POST"])
def remove_bookmark_in_cafe_details():
    """Remove a bookmark in cafe details page."""

    user_id = session["user_id"]
    cafe_id = request.form.get("cafe-id")
    cafe = crud.get_cafe_by_id(cafe_id)

    bookmark = crud.get_bookmark_by_user_and_cafe_id(user_id, cafe_id)
    db.session.delete(bookmark)
    db.session.commit()

    flash(f"You have successfully removed {cafe.name} from My Bookmarks.")
    return redirect(f"/cafe/{cafe_id}")


@app.route("/mybookmarks")
def bookmarks_page():
    """View all user bookmarks."""

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    bookmarks = crud.get_all_user_bookmarks(user_id)

    return render_template("bookmarks.html", user=user, bookmarks=bookmarks)


@app.route("/mybookmarks/removebookmark", methods=["POST"])
def remove_bookmark_in_bookmarks():
    """Remove a bookmark in bookmarks page."""

    user_id = session["user_id"]
    cafe_id = request.form.get("cafe-id")
    cafe = crud.get_cafe_by_id(cafe_id)

    bookmark = crud.get_bookmark_by_user_and_cafe_id(user_id, cafe_id)
    db.session.delete(bookmark)
    db.session.commit()

    flash(f"You have successfully removed {cafe.name} from My Bookmarks.")
    return redirect("/mybookmarks")


### ROUTES FOR NOTES ###
@app.route("/note/<bookmark_id>", methods=["POST"])
def add_note(bookmark_id):
    """Create a note for a bookmark.

    Three options for a note:
    1. Create a new note.
    2. Update a note.
    3. Delete a note.

    - To create a new note, we need to make sure a note does not exist already.
    - If a note exists and the updated note is not empty, we can update the note.
    - If a note exists and the updated note is empty, we can delete the note. 
    """

    existing_note = crud.get_note_by_bookmark_id(bookmark_id)
    cafe = crud.get_cafe_by_bookmark_id(bookmark_id)
    user_id = session["user_id"]
    note = request.form.get("cafe-note")

    if not existing_note:
        new_note = crud.create_note(user_id, bookmark_id, note)
        db.session.add(new_note)
        db.session.commit()

    elif existing_note and note != "":
        crud.update_note(existing_note, note)

    elif existing_note and note == "":
        crud.delete_note(existing_note)

    flash(f"You have successfully saved your note for {cafe.name}.")
    return redirect("/mybookmarks")
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
