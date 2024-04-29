"""
Routes for a Flask web application
handling user requests, data retrieval and manipulation,
user authentication, and access control
"""

#import required modules
from app import app
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
import users
from db import db
import db_operations


@app.route("/", methods=["GET", "POST"])
def index():
    """
    main page, includes login function
    """
    if request.method == "GET":
        return render_template("index.html")#login form

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Incorrect username or password")
        return redirect("/")


@app.route("/result", methods=["GET"])
def result():
    """
    search function, searches all results in school listing, including city, description and name
    """
    query = request.args["query"]
    messages = db_operations.fetch(query)
    return render_template("result.html", query=query, messages=messages)



@app.route("/logout")
def logout():
    """
    logout
    """
    users.logout()
    return redirect("/")


@app.route("/register", methods=["get", "post"])
def register():
    """
    register
    """
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Username needs to be between 1 and 20 characters long")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords don't match")
        if password1 == "":
            return render_template("error.html", message="Password is empty")

        role = int(request.form["role"])
        if role not in (1,2):
            return render_template("error.html", message="Unknown user role")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Unsuccessful registration")
        return redirect("/")


@app.route("/dance_schools")
def dance_schools():
    """
    listing page for dance schools
    """
    list = db_operations.get_school_list()
    #is the session logged in with admin rights:
    if session.get("user_role") == 2:
        return render_template("dance_schools.html", add_button=True, count=len(list), messages=list, delete_button=True)
    return render_template("dance_schools.html", add_button=False, count=len(list), messages=list, delete_button=False)



@app.route("/add_dance_school")
def add_dance_school():
    """
    add dance schools
    """
    if session.get("user_role") == 2:
        return render_template("add_dance_school.html")
    else:
        return render_template("error.html", message="Not allowed")

@app.route("/send_school", methods=["POST"])
def send():
    name = request.form["name"]
    city = request.form["city"]
    description = request.form["description"]
    url= request.form["url"]
    #new school
    if db_operations.add_school(name, city, description, url):
        return redirect("/dance_schools")
    else:
        return render_template("error.html", message="unsuccessful")

@app.route("/delete_school/<int:id>", methods=["POST"])
def delete_school(id):
    db_operations.delete_school(id)
    return redirect("/dance_schools")

@app.route("/school/<int:id>")
def school(id):
    """
    show one school
    """
    school = db_operations.view_school(id)
    name = school[0]
    location = school[1]
    description = school[2]
    reviews = school[3]
    url = school[5]
    if session.get("user_role") == 2:
        return render_template("view_school.html", id=id, name=name, location=location, description=description, \
                           reviews=reviews, add_button=True, url=url)
    return render_template("view_school.html", id=id, name=name, location=location, description=description, \
                           reviews=reviews, add_button=False, url=url)

@app.route("/<int:id>/add_review")
def review(id):
    """
    add review
    """
    if "user_name" in session:
        name = db_operations.fetch_school_name(id)
        return render_template("review.html", id=id, name=name)
    return render_template("error.html", message="You need to be logged in to add a review")


@app.route("/send_review/<int:id>", methods=["POST"])
def send_review(id):
    rating = int(request.form["rating"])
    comment = request.form["comment"]

    if not rating:
        return render_template("error.html", message="Please select a rating")
    if len(comment) > 5000:
        return render_template("error.html", message="The review you entered is too long")
    rating = int(rating)
    if db_operations.add_review(id, rating, comment):
        return redirect(f"/school/{id}")
    else:
        return render_template("error.html", message="unsuccessful")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    db_operations.delete_review(id)
    return redirect("/dance_schools")

@app.route("/forum")
def forum():
    """
    forum main page
    """
    if "user_name" in session:
        list = db_operations.get_chat_list()
        return render_template("forum.html", count=len(list), messages=list)
    return render_template("error.html", message="You need to be logged in to view chats")

@app.route("/new_chat")
def new_chat():
    """
    add new chat on forum
    """
    return render_template("new_chat.html")

@app.route("/send_chat", methods=["POST"])
def send_chat():
    """
    send new chat on forum
    """
    if "user_name" in session:
        user_id = users.user_id()
        content = request.form["content"]
        if db_operations.send_chat(user_id, content):
            return redirect("/forum")
        else:
            return render_template("error.html", message="Sending failed")
