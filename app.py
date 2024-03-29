from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
#määritä osoite jonka kautta tietokantaan saadaan yhteys
#luo db olio
#    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///juliarahkonen"
#käytetään mielummin ympäristömuuttujaa:
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)#anna lista jossa rivit


#kirjautumistiedot

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


#viestien lähetys sivulle

@app.route("/messages")
def messages():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("messages.html", count=len(messages), messages=messages) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    #lisää uusi rivi kun käyttäjä on lähettänyt viestin lomakkeella
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    #commit tehtävä jotta transaktio viedään loppuun ja muutokset menevät pysyvästi tietokantaan
    db.session.commit()
    #palataan lomakkeen lähetyksen jälkeen takaisin etusivulle
    #ettei käyttäjä lähetä vahingossa samaa lomaketta uudestaan
    return redirect("/")

#hakutoiminto:

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = text("SELECT id, content FROM messages WHERE content LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return render_template("result.html", query=query, messages=messages)

#kävijöiden vierailuaika:

@app.route("/visitors")
def visitors():
    db.session.execute(text("INSERT INTO visitors (time) VALUES (NOW())"))
    db.session.commit()
    result = db.session.execute(text("SELECT COUNT(*) FROM visitors"))
    counter = result.fetchone()[0]
    return render_template("visitors.html", counter=counter) 

#muut:

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)