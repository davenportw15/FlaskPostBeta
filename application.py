"""
This is a sample application to become familiar with Flask
"""

from flask import Flask, request, session, render_template, url_for, redirect, flash
from sqlite3 import connect
from models.users import Users
from models.posts import Posts
from models.admin import Admin
import os

app = Flask(__name__)
connection = connect(
    "%s/models/db.sqlite3" % (os.path.dirname(os.path.realpath(__file__))),
    check_same_thread=False
)
users = Users(connection)
posts = Posts(connection)
admin = Admin(connection)

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
            flash("The username %s has already been taken" % request.form["username"])
            return redirect(url_for("new_user"))

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
        return render_template("view_user.html", posts=posts, username=session["username"], me=True)
    else:
        return redirect(url_for("login"))

@app.route("/user/<username>")
def view_user(username):
    if "username" in session and session["username"] == username:
        return redirect(url_for("me"))
    elif users.user_exists(username):
        return render_template("view_user.html", posts=posts, username=username, me=False)
    else:
        return render_template("user_not_found.html", username=username)

@app.route("/post", methods=["GET", "POST"])
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

@app.route("/post/<post_number>")
def view_post(post_number):
    if posts.post_exists(post_number):
        return render_template("view_post.html", post=posts.get_post_by_id(post_number))
    else:
        return render_template("post_not_found.html", id=post_number)

@app.route("/admin")
def list_users():
    if "username" in session:
        if admin.admin_exists(session["username"]):
            return render_template("admin_list_users.html", users=users)
        else:
            flash("%s is not an administrator" % session["username"])
            return redirect(url_for("login"))
    else:
        flash("Log in as an administrator to access that page")
        return redirect(url_for("login"))

@app.route("/delete_user", methods=["POST"])
def delete_user():
    if users.user_exists(request.form["username"]):
        users.delete_user(request.form["username"])
        posts.delete_posts_by_user(request.form["username"])
        return redirect(url_for("list_users"))

@app.route("/delete_post", methods=["POST"])
def delete_post():
    if posts.post_exists(request.form["id"]):
        posts.delete_post_by_id(request.form["id"])
        return redirect(url_for("me"))

@app.route("/about")
def about():
    return render_template("about.html")


#Errors
@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404

#Start the server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
