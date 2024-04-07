from app import app
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
import users
from db import db


@app.route("/")
def index():
    return render_template("index.html")

#viestien lähetys sivulle

@app.route("/messages")
def messages():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("messages.html", count=len(messages), messages=messages) 

#hakutoiminto:

@app.route("/search")
def form():
    return render_template("form.html")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = text("SELECT id, content FROM schools WHERE description LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return render_template("result.html", query=query, messages=messages)


#muut:

"""@app.route("/dance_schools")
def page1():
    return render_template("dance_schools.html")

@app.route("/dance_events")
def page2():
    return render_template("dance_events.html")"""

#kirjautuminen:

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

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

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

#lisää kouluja:

@app.route("/dance_schools")
def dance_schools():
    #ollaanko kirjauduttu admin oikeuksilla
    if session.get("user_role") == 2:
        return render_template("add_dance_school.html")
    else:
        return render_template("dance_schools.html")

@app.route("/add_dance_school", methods=["POST"])
def add_dance_school():
    if session.get("user_role") == 2:
        name = request.form["name"]
        rating = int(request.form["rating"])
        dance_type = request.form["dance_type"]
        
        #uusi koulu
        db.session.execute(
            "INSERT INTO schools (name, rating, dance_type) VALUES (:name, :rating, :dance_type)",
            {"name": name, "rating": rating, "dance_type": dance_type}
        )
        db.session.commit()

        return redirect("/dance_schools")
    else:
        return redirect("/")

@app.route("/dance_events")
def dance_events():
    #ollaanko kirjauduttu admin oikeuksilla
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
        
        #uusi eventti
        db.session.execute(
            "INSERT INTO events (name, weekday, description, school_id) VALUES (:name, :weekday, :description, :school_id)",
            {"name": name, "weekday": weekday, "description": description, "school_id": school_id}
        )
        db.session.commit()

        return redirect("/dance_events")
    else:
        return redirect("/")