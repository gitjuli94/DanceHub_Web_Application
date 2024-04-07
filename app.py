from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import routes




"""if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)"""