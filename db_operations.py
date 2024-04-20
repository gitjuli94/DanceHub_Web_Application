from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def add_school(name, city, description):
    sql = "INSERT INTO schools (name, city, description) VALUES (:name, :city, :description)"
    db.session.execute(text(sql), {"name": name, "city": city, "description": description})
    #"INSERT INTO schools (name, city, description) VALUES (:name, :city, :description)",
    #{"name": name, "city": city, "description": description}
    #))
    db.session.commit()
    return True

def get_school_list():
    sql = "SELECT s.name, s.description, " \
          "COALESCE(CAST(AVG(CASE WHEN r.rating IS NULL THEN NULL ELSE r.rating END) AS TEXT), '-') AS avg_rating, " \
          "s.city FROM schools s " \
          "LEFT JOIN reviews r ON s.id = r.school_id " \
          "GROUP BY s.id, s.name, s.description, s.city " \
          "ORDER BY avg_rating DESC;"
    result = db.session.execute(text(sql))
    return result.fetchall()

