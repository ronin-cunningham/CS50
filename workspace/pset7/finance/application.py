from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import time

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    symbols_in_portfolio = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id", id=session["user_id"])


    money_total = 0


    for i in symbols_in_portfolio:
        symbol = i["symbol"]
        shares = i["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        money_total += total
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(stock["price"]), total=usd(total), id=session["user_id"], symbol=symbol)


    updated_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    money_total += updated_cash[0]["cash"]

    new_portfolio = db.execute("SELECT * from portfolio WHERE id=:id", id=session["user_id"])

    return render_template("index.html", stocks=new_portfolio, cash=usd(updated_cash[0]["cash"]), total= usd(money_total) )







@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    if request.method == "POST":


        #get stock symbol
        symbol = lookup(request.form.get("entersymbol"))

        #make sure stock is valid

        if not symbol:
            return apology("Invalid ticker symbol")

        #get and make sure number of shares is valid
        try:
            shares = int(request.form.get("numberofshares"))
            if int(shares) < 0:
                return apology("Shares must be a positive number")
        except:
            return apology("shares must be integer")


        #make sure user can afford shares
        usercash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        costofshares = int(symbol["price"])*shares
        if int(costofshares) > usercash[0]["cash"]:
            apology("You do not have enough money to buy the stock")




        #test if user has symbol of shares he/she wishes to buy
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol = :symbol", id=session["user_id"], symbol=request.form.get("entersymbol"))

        #if this is a first time buy and the share symbol is not already in database, add it
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)", name=symbol["name"], shares=shares, price=usd(symbol["price"]), total=usd(costofshares), symbol=symbol["symbol"], id=session["user_id"])

        #if it has bin added before, update the new quantities
        else:
           totaliture_shares = user_shares[0]["shares"] + shares
           db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", shares=totaliture_shares, id=session["user_id"], symbol=symbol["symbol"])

        #update cash by subtracting from their user's table cash row column
        db.execute("UPDATE users SET cash = cash - :costofshares WHERE id = :id", costofshares=costofshares, id=session["user_id"])

        #add transaction to history
        localtime = time.asctime( time.localtime(time.time()) )
        db.execute("INSERT INTO history (id, symbol, shares, quote, time) VALUES(:id, :symbol, :shares, :quote, :time)", id=session["user_id"], symbol=symbol["symbol"], shares=shares, quote=symbol["price"], time=localtime)
        return redirect(url_for("index"))


    else:
        return render_template("buy.html")











@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    history = db.execute("SELECT * FROM histories WHERE id=:id", id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/addcash")
@login_required
def addcash():
    if request.method == "POST":
        amount = request.form.get("morecash")
        if not amount:
            return apology("You didn't enter any number")
        if int(amount) < 0:
            return apology("You want to lose money?")
        current_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=usd(current_cash + request.form.get("morecash"), id=session["user_id"]))

    else:
        return render_template("addcash.html")










@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        #get quote from user input
        quote = lookup(request.form.get("symbol"))

        #if lookup fails and returns false
        if not quote:
            return apology("ticker symbol not valid")

        #finally, return render template of quoted, giving in quote with value python's quote variable
        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    #if method is POST
    if request.method == "POST":

        #ensure fields are entered and not blank
        if not request.form.get("username"):
            apology("Must enter username")

        if not request.form.get("password"):
            apology("Must enter password")

        elif not request.form.get("confirm password"):
            return apology("Must confirm password")

        #make sure passwords match and no typos
        elif request.form.get("password") != request.form.get("confirm password"):
            return apology("passwords do not match!")



        #puts username and hashed password into database and stores result in result variable
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        #if result is false, return an apology saying username already exists
        if not result:
            return apology("Username already exists")

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    #if method is GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    #make sure it is post
    if request.method == "POST":
        #if nothing is in sellsymbol box, return apology
        if not request.form.get("sellsymbol"):
            return apology("enter ticker symbol to sell")
        #if nothing is in amount box, return apology
        if not request.form.get("amount"):
            return apology("enter an amount")
        #lookup symbol
        symbol = lookup(request.form.get("sellsymbol"))
        #if symbol is not a valid symbol, return apology
        if not symbol:
            return apology("symbol not valid")
        #check for symbol in user database, if not there return apology
        usersymbols = db.execute("SELECT symbol FROM portfolio where symbol=:symbol AND id=:id", symbol=request.form.get("sellsymbol"), id=session["user_id"])
        if not usersymbols:
            return apology("you do not have this stock")

        #check if sell amount is a positive integer
        if int(request.form.get("amount")) < 0:
            return apology("amount must be positive integer")

        #establish amount of shares variable
        amount = db.execute("SELECT shares FROM portfolio where symbol=:symbol AND id=:id", symbol=request.form.get("sellsymbol"), id=session[user_id])

        #check if user has enough stock of symbol to sell
        if int(request.form.get("amount")) > amount:
            return apology("you do not have enough stock to sell desired amount")

        #establish a final amount of shares variable
        finalamount = amount - request.form.get("amount")

        #update amount of shares user has in database to equal final amount
        db.execute("UPDATE portfolio SET shares=:shares", shares=finalamount)

        #if final amount of shares is 0, might as well remove if from database
        if finalamount == 0:
            db.execute("DELETE FROM portfolio WHERE symbol=:symbol", symbol=request.form.get("sellsymbol"))

        #find out stockworth
        stockworth = request.form.get("amount") * symbol["price"]

        #find out current amount of user's cash
        current_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

        #update user's cash
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=usd(current_cash + stockworth), id=session["user_id"])

        #set time when'st this happened
        localtime = time.asctime( time.localtime(time.time()) )
        #update history
        db.execute("INSERT INTO histories (symbol, shares, price, id, time) VALUES(:symbol, :shares, :price, :id, :time)", symbol=stock["symbol"], shares =-request.form.get("amount"), price=usd(symbol["price"]), id=session["user_id"], time=localtime)
    else:
        return render_template("sell.html")
