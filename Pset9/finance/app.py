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

    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    # Initiate the variable
    total = cash
    # Calculate the sum of remaining cash and bought shares
    for stock in stocks:
        total += stock["price"] * stock["shares"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if not symbol:
            return apology("missing symbol")

        if not request.form.get("shares"):
            return apology("missing shares")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("amount of shares invalid (code 1)")

        if shares <= 0:
            return apology("amount of shares invalid (code 2)")

        if not stock:
            return apology("invalid symbol")

        else:

            user_id = session["user_id"]
            # This returns a dictionary with key value pairs, ransforms key value pair and only safes the actual cash value
            user_cash = db.execute("SELECT cash FROM users WHERE id LIKE ?", user_id)[0]["cash"]

            name = stock["name"]
            price = stock["price"]
            # Price of intended purchase that is deducted if enough money remaining
            total_price = shares * price

            if user_cash < total_price:
                return apology("Not enough money")

            else:
                user_cash_new = user_cash - total_price

                # Update the users remaining cash
                db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash_new, user_id)
                # Insert new line into the transactions table
                db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, type) VALUES(?, ?, ?, ?, ?, ?)", user_id, symbol, name, shares, price, 'buy')
                # Use flash according to its documentation
                flash("Bought!")

                return redirect ("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, date, type FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transactions=transactions, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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
            return apology("invalid symbol")

        else:
            # Renders the designated templed and passes a variable result, that is set equal to result from request form
            return render_template("quoted.html", stock = stock, usd=usd)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure a username is entered
        if not request.form.get("username"):
            return apology("must enter username")

        # Ensure a password is entered
        elif not request.form.get("password"):
            return apology("must enter password")

        # Ensure the password confirmation is entered
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Make sure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Ensure username does not exist in database yet
            if len(rows) == 1:
                return apology("username is already in use")

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


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Change password"""

    if request.method == "POST":

        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure the old password is entered
        if not request.form.get("oldpw"):
            return apology("must enter old password")

        # Ensure the old password matches with the users current password
        elif not check_password_hash(rows[0]["hash"], request.form.get("oldpw")):
            return apology("old password does not match user")

        # Ensure a new password is entered
        elif not request.form.get("newpw"):
            return apology("must enter new password")

        # Ensure the password confirmation is entered
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Make sure password and confirmation match
        elif request.form.get("newpw") != request.form.get("confirmation"):
            return apology("passwords do not match")

        else:
            # Generate password hash
            hash = generate_password_hash(request.form.get("newpw"))

            # Insert new user into the database
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

            flash("Password updated!")

            return redirect("/")

    # User reached route via GET
    else:
        return render_template("changepw.html")


@app.route("/success", methods=["GET"])
def success():
    """Auto-redirect to Log In after 3 seconds"""

    return render_template("success.html"), {"Refresh": "3; url=/login"}


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        # Define all necessary variables and optain them from db or lookup
        user_id = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        share_name = lookup(symbol)["name"]
        share_price = lookup(symbol)["price"]
        total_price = shares * share_price

        shares_owned = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["shares"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Make sure all conditions are met
        if not symbol:
            return apology("missing symbol")

        if shares <= 0:
            return apology("amount of shares invalid")

        if shares > shares_owned:
            return apology("not enough shares available")

        # Update users table with new cash value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash + total_price, user_id)
        # Update transactions table and substract sold shares from owned shares --> "-shares"
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", user_id, share_name, -shares, share_price, 'sell', symbol)

        # Use flash according to its documentation
        flash("Sold!")

        return redirect("/")

    # User reached route via GET
    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)