from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def add_school(name, city, description, url):
    sql = "INSERT INTO schools (name, city, description, visible, url) VALUES (:name, :city, :description, :visible, :url)"
    db.session.execute(text(sql), {"name": name, "city": city, "description": description, "visible": True, "url": url})
    db.session.commit()
    return True

def delete_school(id):
    sql = "UPDATE schools SET visible=FALSE WHERE schools.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def get_school_list():
    sql = "SELECT s.id, s.name, s.description, " \
          "COALESCE(CAST(ROUND(AVG(CASE WHEN r.visible = TRUE THEN r.rating ELSE NULL END), 1) AS TEXT), '-') AS avg_rating, " \
          "s.city FROM schools s " \
          "LEFT JOIN reviews r ON s.id = r.school_id " \
          "WHERE s.visible = TRUE " \
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
    sql = "SELECT name, city, description, url FROM schools WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    school = result.fetchone()
    name = school[0]
    location = school[1]
    description = school[2]
    url = school[3]
    sql = "SELECT * FROM reviews WHERE school_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    reviews = result.fetchall()
    return [name, location, description, reviews, id, url]

def add_review(id, rating, comment):
    sql = "INSERT INTO reviews (school_id, rating, comment, visible) VALUES (:school_id, :rating, :comment, :visible)"
    db.session.execute(text(sql), {"school_id":id, "rating": rating, "comment": comment, "visible": True})
    db.session.commit()
    return True

def delete_review(id):
    sql = "UPDATE reviews SET visible=FALSE WHERE reviews.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

"""dance styles, provided automatically in the database?"""
def add_styles():
    styles = ['Ballet', 'Hip Hop', 'Jazz', 'Contemporary', 'Tap', 'Ballroom', 'Salsa', 'Bachata', 'Swing', 'Tango', 'Latin']
    for style in styles:
        sql = text("INSERT INTO styles (name) VALUES (:style)")
        db.session.execute(sql, {'style': style})
    db.session.commit()
    return True


def fetch(query):
    sql = """
    SELECT id, name, description, city FROM schools
    WHERE (lower(name) LIKE lower(:query)
    OR lower(city) LIKE lower(:query)
    OR lower(description) LIKE lower(:query))
    AND visible = TRUE;
    """
    result = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return result.fetchall()
