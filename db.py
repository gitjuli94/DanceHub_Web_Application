"""
initialize Flask application and connect to database
"""

#import required modules
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app



#connect to database:
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
#create database object
db = SQLAlchemy(app)#give list

def initialize_database():
    """
    let's initialize the database with built in dance styles and an example school
    """
    #list of dance styles
    dance_styles = [
        'Ballet', 'Hip Hop', 'Jazz', 'Contemporary', 'Tap',
        'Ballroom', 'Salsa', 'Bachata', 'Swing', 'Tango', 'Latin'
    ]


    #the dance styles if they don't yet exist (=if the app is initialized for the 1st time)
    for style in dance_styles:
        sql = "INSERT INTO styles (name) VALUES (:style) ON CONFLICT (name) DO NOTHING"
        db.session.execute(text(sql), {"style": style})

    #create example school
    name= "Example_School"
    city = "Helsinki"
    description = "A school founded in 2024"
    url = "www.exampleschool.com"
    sql = """
            INSERT INTO schools (name, city, description, visible, url) VALUES (:name, :city, :description, :visible, :url)
            ON CONFLICT (url) DO NOTHING
        """
    db.session.execute(text(sql), {"name": name, "city": city, "description": description, "visible": True, "url": url})
    #commit changes to the database
    db.session.commit()


