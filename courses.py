from db import db
from flask import session
from sqlalchemy.sql import text
import urllib.parse

def create_course(name, teacher, description):
    try:
        sql = text("INSERT INTO courses (name, teacher, description) VALUES (:name, :teacher, :description)")
        db.session.execute(sql, {"name":name, "teacher":teacher, "description":description})
        db.session.commit()
        return True
    except:
        return False


def add_characters(character, transliteration, course_id):
    if not character or not transliteration:
        return False
    try:
        sql = text("""INSERT INTO characters (character, transliteration, course_id)
                      VALUES (:character, :transliteration, :course_id)""")
        db.session.execute(sql, {"character":character, "transliteration":transliteration, "course_id":course_id})
        db.session.commit()
        return True
    except:
        return False

def add_words(word, translation, course_id):
    if not word or not translation:
        return False
    try:
        sql = text("""INSERT INTO words (word, translation, course_id)
                      VALUES (:word, :translation, :course_id)""")
        db.session.execute(sql, {"word":word, "translation":translation, "course_id":course_id})
        db.session.commit()
        return True
    except:
        return False

def add_material(material, course_id):
    if not material:
        return False
    try:
        sql = text("""INSERT INTO course_material (material, course_id)
                      VALUES (:material, :course_id)""")
        db.session.execute(sql, {"material":material, "course_id":course_id})
        db.session.commit()
        return True
    except:
        return False


def course_id(name):
    sql = text("SELECT id FROM courses WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    course_id = result.fetchone()
    if course_id is not None:
        return course_id[0]

def encode_parameter(course_name):
    return urllib.parse.quote(course_name)

def decode_url(url_course_name):
    return urllib.parse.unquote(url_course_name)

def course_teacher(name):
    sql = text("SELECT teacher FROM courses WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    teacher = result.fetchone()
    if teacher is not None:
        return teacher[0]


def return_courses():
    sql = text("SELECT name, teacher, description FROM courses")
    result = db.session.execute(sql)
    courses = result.fetchall()
    if courses is not None:
        return courses

def return_own_courses(teacher):
    sql = text("SELECT name FROM courses WHERE teacher=:teacher")
    result = db.session.execute(sql, {"teacher":teacher})
    courses = result.fetchall()
    return courses

def return_course_words(course_id):
    sql = text("SELECT word, translation FROM words WHERE course_id=:course_id")
    result = db.session.execute(sql, {"course_id":course_id})
    words = result.fetchall()
    return words

def return_course_characters(course_id):
    sql = text("SELECT character, transliteration FROM characters WHERE course_id=:course_id")
    result = db.session.execute(sql, {"course_id":course_id})
    characters = result.fetchall()
    return characters
