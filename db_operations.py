from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def add_school(name, city, description):
    sql = "INSERT INTO schools (name, city, description) VALUES (:name, :city, :description)"
    db.session.execute(text(sql), {"name": name, "city": city, "description": description})
    db.session.commit()
    return True

def get_school_list():
    sql = "SELECT s.id, s.name, s.description, " \
          "COALESCE(CAST(ROUND(AVG(CASE WHEN r.rating IS NULL THEN NULL ELSE r.rating END), 1) AS TEXT), '-') AS avg_rating, " \
          "s.city FROM schools s " \
          "LEFT JOIN reviews r ON s.id = r.school_id " \
          "GROUP BY s.id, s.name, s.description, s.city " \
          "ORDER BY avg_rating DESC;"
    result = db.session.execute(text(sql))
    return result.fetchall()


def fetch_school_name(id):
    sql = "SELECT name FROM schools WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    name = result.fetchone()
    return name[0] if name else None

def view_school(id):
    sql = "SELECT name, city, description FROM schools WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    school = result.fetchone()
    name = school[0]
    location = school[1]
    description = school[2]
    sql = "SELECT * FROM reviews WHERE school_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    reviews = result.fetchall()
    return [name, location, description, reviews, id]

def add_review(id, rating, comment):
    sql = "INSERT INTO reviews (school_id, rating, comment) VALUES (:school_id, :rating, :comment)"
    db.session.execute(text(sql), {"school_id":id, "rating": rating, "comment": comment})
    db.session.commit()
    return True

