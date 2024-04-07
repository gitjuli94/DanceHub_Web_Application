from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


#määritä osoite jonka kautta tietokantaan saadaan yhteys
#luo db olio
#    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///juliarahkonen"
#käytetään mielummin ympäristömuuttujaa:


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)#anna lista jossa rivit