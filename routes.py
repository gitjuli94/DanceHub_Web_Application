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


"""#search function:"""

@app.route("/search")
def form():
    return render_template("form.html")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = text("SELECT id, content FROM schools WHERE description LIKE :query")
    result_set = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result_set.fetchall()
    return render_template("result.html", query=query, messages=messages)


"""#log in:"""

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

"""#log out:"""
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

"""#register:"""
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


"""@app.route("/dance_events")
def dance_events():
    #is the session logged in with admin rights:
    if session.get("user_role") == "2":
        return render_template("add_dance_event.html")
    else:
        return render_template("dance_events.html")

@app.route("/add_dance_event", methods=["POST"])
def add_dance_event():
    if session.get("user_role") == "2":
        name = request.form["name"]
        weekday = request.form["weekday"]
        description = request.form["description"]
        school_id = int(request.form["school_id"])

        #new event
        db.session.execute( #this modified into two lines because long
            "INSERT INTO events (name, weekday, description, school_id) " \
            "VALUES (:name, :weekday, :description, :school_id)",
            {"name": name, "weekday": weekday, "description": description, "school_id": school_id}
        )
        db.session.commit()

        return redirect("/dance_events")
    else:
        return redirect("/")"""
