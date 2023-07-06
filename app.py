"""Server for Coffee Notes app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud


app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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


@app.route("/dashboard")
def dashboard_page():
    """View user dashboard."""

    if "user_id" in session:
        return render_template("dashboard.html", name=session["name"])
    return redirect("/")


@app.route("/profile/<user_id>")
def profile_page(user_id):
    """View user profile page."""

    user = crud.get_user_by_id(user_id)

    return render_template("profile.html", user=user)


@app.route("/cafe/<cafe_id>")
def cafe_page(cafe_id):
    """View details of a cafe."""

    cafe = crud.get_cafe_by_id(cafe_id)

    return render_template("cafe_details.html", cafe=cafe)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")