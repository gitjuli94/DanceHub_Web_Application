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

"""main page"""
@app.route("/")
def index():
    return render_template("index.html")


"""search function, not finished:"""

@app.route("/result")
def result():
    query = request.args["query"]
    messages = db_operations.fetch(query)
    return render_template("result.html", query=query, messages=messages)


"""log in:"""

@app.route("/login", methods=["get", "post"])#login
def login():
    if request.method == "GET":
        return render_template("login.html")#login

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

"""log out:"""
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

"""register:"""
@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        role = int(request.form["role"])
        if role not in (1,2):
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

"""main page for dance schools"""

@app.route("/dance_schools")
def dance_schools():
    list = db_operations.get_school_list()
    #is the session logged in with admin rights:
    if session.get("user_role") == 2:
        return render_template("dance_schools.html", add_button=True, count=len(list), messages=list)
    return render_template("dance_schools.html", add_button=False, count=len(list), messages=list)

"""add dance schools"""

@app.route("/add_dance_school")
def add_dance_school():
    if session.get("user_role") == 2:
        return render_template("add_dance_school.html")
    else:
        return render_template("error.html", message="Not allowed")

@app.route("/send_school", methods=["POST"])
def send():
    name = request.form["name"]
    city = request.form["city"]
    description = request.form["description"]
    #new school
    if db_operations.add_school(name, city, description):
        #return redirect("/dance_schools")
        return redirect("/")
    else:
        return render_template("error.html", message="unsuccessful")


"""show school"""
@app.route("/school/<int:id>")
def school(id):
    school = db_operations.view_school(id)
    name = school[0]
    location = school[1]
    description = school[2]
    reviews = school[3]
    return render_template("view_school.html", id=id, name=name, location=location, description=description, reviews=reviews)

"""add review"""
@app.route("/<int:id>/add_review")
def review(id):
    if "user_name" in session:
        name = db_operations.fetch_school_name(id)
        return render_template("review.html", id=id, name=name)
    return render_template("error.html", message="You need to be logged in to add a review")


@app.route("/send_review/<int:id>", methods=["POST"])
def send_review(id):
    rating = int(request.form["rating"])
    comment = request.form["comment"]
    if db_operations.add_review(id, rating, comment):
        return redirect(f"/school/{id}")
    else:
        return render_template("error.html", message="unsuccessful")


"""main page for dance schedules, sorted by city"""
"""
@app.route("/schedules")
def schedules():
    list = db_operations.get_schedules()
    #is the session logged in with admin rights:
    if session.get("user_role") == 2:
        return render_template("dance_schools.html", add_button=True, count=len(list), messages=list)
    return render_template("dance_schools.html", add_button=False, count=len(list), messages=list)

#add schedules#

@app.route("/add_schedules")
def add_dance_school():
    if session.get("user_role") == 2:
        return render_template("add_dance_school.html")
    else:
        return render_template("error.html", message="Not allowed")

@app.route("/send_schedule", methods=["POST"])
def send():
    name = request.form["name"]
    city = request.form["city"]
    description = request.form["description"]
    #new schedule
    if db_operations.add_school(name, city, description):
        return redirect("/")
    else:
        return render_template("error.html", message="unsuccessful")"""
