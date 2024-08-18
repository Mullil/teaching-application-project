   
CREATE TABLE teachers (
	id SERIAL PRIMARY KEY,
       	username TEXT UNIQUE,
       	password TEXT
);

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
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
       	description TEXT,
	url_name TEXT
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

CREATE TABLE enrollments (
	user_id INT NOT NULL,
	course_id INT NOT NULL,
	exercise1 INT,
	exercise2 INT,
	PRIMARY KEY (user_id, course_id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (course_id) REFERENCES courses(id)
);



