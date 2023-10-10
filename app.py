import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

app.static = 'images'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    error_message = None

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            error_message = "Must provide an email"

        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "Must provide a password"

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error_message = "invalid email and/or password"

        if error_message != None:
            return render_template("login.html", error_message=error_message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Welcome!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    error_message = None

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not email:
            error_message = "Must provide an email."

        if not password:
            error_message = "Must provide a password."

        if not confirmation:
            error_message = "You must confirm your password."

        if password != confirmation:
            error_message = "The password and confirmation password don't match."

        if len(rows) != 0:
            error_message = "Email already exists. Please enter a new email."

        if error_message != None:
            return render_template("register.html", error_message=error_message)

        db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        session["user_id"] = rows[0]['id']
        # Redirect user to home page
        flash("Registered!")
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change user password"""

    error_message = None

    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")
        new_password = request.form.get("new")

        if not email:
            error_message = "Must provide an email."

        actual_db = db.execute("SELECT * FROM users WHERE email = ?", email)

        if not password or not new_password or not request.form.get("confirmation") or not check_password_hash(actual_db[0]["hash"], password):
            error_message = "Must provide correct passwords."

        if error_message != None:
            return render_template("change.html", error_message=error_message)

        db.execute("UPDATE users SET hash = ? WHERE email = ?", generate_password_hash(new_password), email)
        flash("Changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/roadmaps", methods=["GET", "POST"])
def roads():
    """Skills roadmaps"""

    return render_template("roads.html")


@app.route("/videos", methods=["GET", "POST"])
def vids():
    """Skills roadmaps"""

    return render_template("videos.html")

@app.route("/graphic", methods=["GET", "POST"])
def graphic():
    """Graphic design roadmaps"""

    return render_template("graphic.html")

@app.route("/uiux", methods=["GET", "POST"])
def uiux():
    """UI/UX design roadmaps"""

    return render_template("uiux.html")

@app.route("/motion", methods=["GET", "POST"])
def motion():
    """Motion design roadmaps"""

    return render_template("motion.html")

@app.route("/video-editing", methods=["GET", "POST"])
def videdit():
    """Motion design roadmaps"""

    return render_template("videdit.html")

@app.route("/logo", methods=["GET", "POST"])
def logo():
    """Logo design roadmaps"""

    return render_template("logo.html")

@app.route("/packaging", methods=["GET", "POST"])
def packaging():
    """packaging design roadmaps"""

    return render_template("packaging.html")

@app.route("/3d-art", methods=["GET", "POST"])
def dart():
    """3d art roadmaps"""

    return render_template("dart.html")

@app.route("/print", methods=["GET", "POST"])
def print():
    """Print design roadmaps"""

    return render_template("print.html")

@app.route("/nft", methods=["GET", "POST"])
def nft():
    """NFT art roadmaps"""

    return render_template("nft.html")

@app.route("/animation", methods=["GET", "POST"])
def animation():
    """animation roadmaps"""

    return render_template("animation.html")

@app.route("/web", methods=["GET", "POST"])
def web():
    """web design roadmaps"""

    return render_template("web.html")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')  