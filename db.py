"""
initialize Flask application and connect to database
"""

#import required modules
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app



#connect to database:
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#create database object
db = SQLAlchemy(app)#give list
