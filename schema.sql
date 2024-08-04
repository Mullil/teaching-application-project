   
CREATE TABLE teachers (
	id SERIAL PRIMARY KEY.
       	username TEXT UNIQUE,
       	password TEXT
);

CREATE TABLE users (
	id SERIAL PRIMARY KEY.
       	username TEXT UNIQUE,
       	password TEXT
);

CREATE TABLE usernames(
	id SERIAL PRIMARY KEY,
       	username TEXT UNIQUE
);

CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
       	name TEXT UNIQUE,
       	teacher TEXT,
       	description TEXT
);

CREATE TABLE course_material (
	id SERIAL PRIMARY KEY,
       	material TEXT,
       	course_id INTEGER REFERENCES courses
);

CREATE TABLE words (
	id SERIAL PRIMARY KEY,
       	word TEXT,
       	translation TEXT,
       	course_id INTEGER REFERENCES courses
);

CREATE TABLE characters (
	id SERIAL PRIMARY KEY,
       	character TEXT,
       	transliteration TEXT,
       	course_id INTEGER REFERENCES courses
);


