"""Server for Coffee Notes app."""

from flask import Flask, render_template
from jinja2 import StrictUndefined
from model import connect_to_db


app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage(): 
    "Return homepage."

    return render_template("homepage.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")