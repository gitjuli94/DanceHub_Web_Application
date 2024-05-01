"""
This module initializes a Flask application and sets a secret key.
"""

#import required modules
from os import getenv
from flask import Flask


#initialize flask, set secret key
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import db
import routes


with app.app_context():
    db.initialize_database()
