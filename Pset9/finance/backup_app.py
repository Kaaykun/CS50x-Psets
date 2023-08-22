import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # "name": quote["companyName"],
    # "price": float(quote["latestPrice"]),
    # "symbol": quote["symbol"]
    user_id = session["user_id"]

    rows = int(db.execute("SELECT COUNT(user_id) FROM transactions WHERE user_id = ?", user_id))
    db_data = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    cursor = 0

    if cursor <= rows:
        symbol = db_database[cursor]["symbol"]

        cursor = cursot + 1
    symbol = db_data[]
    shares =
    price =
    total =


    return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""


    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol.upper())

        if not symbol:
            return apology("missing symbol", 400)

        if not request.form.get("shares"):
            return apology("missing shares", 400)

        shares = int(request.form.get("shares"))

        if shares < 0:
            return apology("missing shares", 400)

        if not stock:
            return apology("invalid symbol", 400)

        else:
            # Price of intended purchase that is deducted if enough money remaining
            transaction_price = shares * stock["price"]
            user_id = session["user_id"]
            # This returns a dictionary with key value pairs
            user_cash_temp = db.execute("SELECT cash FROM users WHERE id LIKE ?", user_id)
            # Transforms key value pair and only safes the actual cash value
            user_cash = user_cash_temp[0]["cash"]

            if user_cash < transaction_price:
                return apology("Not enough money", 400)

            else:
                user_cash_new = user_cash - transaction_price

                # Update the users remaining cash
                db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash_new, user_id)
                # Get current time, imported "datetime" according to its documentation
                date = datetime.datetime.now()
                # Insert new line into the transactions table
                db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)", user_id, stock["symbol"], shares, stock["price"], date)
                # Use flash according to its documentation
                flash("Bought!")

                return redirect ("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Call Lookup on the users input and store the results in a variable
        # Entering an existing symbol returns a list of 3 comma separated values
        stock = lookup(request.form.get("symbol"))

        # In Python, to check if a list empty we can ask the following
        if not stock:
            return apology("invalid symbol", 400)

        else:
            # Renders the designated templed and passes a variable result, that is set equal to result from request form
            return render_template("quoted.html", stock = stock)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure a username is entered
        if not request.form.get("username"):
            return apology("must enter username", 403)

        # Ensure a password is entered
        elif not request.form.get("password"):
            return apology("must enter password", 403)

        # Ensure the password confirmation is entered
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Make sure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Ensure username does not exist in database yet
            if len(rows) == 1:
                return apology("username is already in use", 403)

            else:
                # Give variables to form submissions and generate password hash
                username = request.form.get("username")
                hash = generate_password_hash(request.form.get("password"))

                # Insert new user into the database
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
                return redirect("/success")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/success", methods=["GET"])
def success():
    """Auto-redirect to Log In after 3 seconds"""

    return render_template("success.html"), {"Refresh": "3; url=/login"}


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
