"""
This is a sample application to become familiar with Flask
"""

from flask import Flask, request, session, render_template, url_for, redirect, flash
from sqlite3 import connect
from models.users import Users
from models.posts import Posts

app = Flask(__name__)
connection = connect("models/db.sqlite3", check_same_thread=False)
users = Users(connection)
posts = Posts(connection)

app.secret_key = "jfk23!,e2ffad~~~~.fad.py"

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("me"))
    else:
        return redirect(url_for("login"))

@app.route("/user/new", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("new_user.html")
    elif request.method == "POST":
        if request.form["username"] and request.form["password"] and not users.user_exists(request.form["username"]):
            users.new_user(request.form["username"], request.form["password"])
            session["username"] = request.form["username"]
            return redirect(url_for("me"))
        else:
            return "Sorry, the username %s has already been taken" % request.form["username"]

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.pop("username", None)
        return render_template("login.html")
    elif request.method == "POST":
        if request.form["username"] and request.form["password"] and users.user_exists(request.form["username"]):
            session["username"] = request.form["username"]
            return redirect(url_for("me"))
        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))

@app.route("/user/me")
def me():
    if "username" in session:
        return render_template("me.html", posts=posts)
    else:
        return redirect(url_for("login"))

@app.route("/user/me/post", methods=["GET", "POST"])
def new_post():
    if "username" in session:
        if request.method == "GET":
            return render_template("new_post.html")
        elif request.method == "POST":
            if request.form["comment"]:
                posts.new_post(session["username"], request.form["comment"])
                return redirect(url_for("me"))
            else:
                flash("Posts cannot be empty.")
                return redirect(render_template("new_post.html"))
    else:
        return redirect(url_for("login"))

#start the server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
