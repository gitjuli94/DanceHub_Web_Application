from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def add_school(name, city, description, url, style_ids):
    sql = "INSERT INTO schools (name, city, description, visible, url) VALUES (:name, :city, :description, :visible, :url)"\
            "RETURNING id"
    result = db.session.execute(text(sql), {"name": name, "city": city, "description": description, "visible": True, "url": url})
    school_id = result.fetchone()[0]

    for style_id in style_ids:
            sql = "INSERT INTO style_groups (school_id, style_id) VALUES (:school_id, :style_id)"
            db.session.execute(text(sql), {"school_id": school_id, "style_id": style_id})

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

def view_style_groups(id):
        #get groups
    sql = """
        SELECT s.name
        FROM styles s
        JOIN style_groups sg ON s.id = sg.style_id
        WHERE sg.school_id = :id
        """
    result = db.session.execute(text(sql), {"id":id})
    styles = result.fetchall()
    return [style[0] for style in styles]


def get_dance_styles():
    #get style names
    sql = text("SELECT id, name FROM styles")
    result = db.session.execute(sql)
    print(result)
    return result.fetchall()


def add_review(id, rating, comment):
    sql = "INSERT INTO reviews (school_id, rating, comment, sent_at, visible) VALUES (:school_id, :rating, :comment, NOW(), :visible)"
    db.session.execute(text(sql), {"school_id":id, "rating": rating, "comment": comment, "visible": True})
    db.session.commit()
    return True

def delete_review(id):
    sql = "UPDATE reviews SET visible=FALSE WHERE reviews.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()


def fetch(query):
    sql = """
    SELECT s.id, s.name, s.description, s.city FROM schools s
    LEFT JOIN style_groups sg ON s.id = sg.school_id
    LEFT JOIN styles st ON sg.style_id = st.id
    WHERE (lower(s.name) LIKE lower(:query)
    OR lower(s.city) LIKE lower(:query)
    OR lower(s.description) LIKE lower(:query)
    OR lower(st.name) LIKE lower(:query))
    AND s.visible = TRUE;
    """
    result = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return result.fetchall()

def get_chat_list():
    sql = text("SELECT M.content, U.name, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def send_chat(user_id, content):
    sql = text("INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

