CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    stars INTEGER,
    comment TEXT
);
CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    dance_type TEXT,  --various dannce styles
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    weekday TEXT NOT NULL,
    description TEXT,
    school_id INTEGER REFERENCES schools(id)
);
