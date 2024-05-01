CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);
CREATE TABLE styles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    description TEXT,
    admin_id INTEGER REFERENCES users(id),
    visible boolean,
    url TEXT UNIQUE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    school_id INTEGER REFERENCES schools(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    sent_at TIMESTAMP,
    sent_by INTEGER REFERENCES users(id),
    visible BOOLEAN
);

CREATE TABLE style_groups (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id),
    style_id INTEGER REFERENCES styles(id),
    CONSTRAINT unique_pair UNIQUE (school_id, style_id)
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users(id),
    sent_at TIMESTAMP
);
