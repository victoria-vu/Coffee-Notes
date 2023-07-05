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
            return redirect("/")
    return redirect("/login")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")