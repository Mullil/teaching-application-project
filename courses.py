from db import db
from flask import session
from sqlalchemy.sql import text
import urllib.parse

def create_course(name, teacher, description):
    if len(name) > 50:
        return False
    if not name:
        return False
    try:
        url_name = encode_parameter(name)
        sql = text("INSERT INTO courses (name, teacher, description, url_name) VALUES (:name, :teacher, :description, :url_name)")
        db.session.execute(sql, {"name":name, "teacher":teacher, "description":description, "url_name":url_name})
        db.session.commit()
        return True
    except:
        return False


def add_characters(character, transliteration, course_id):
    if not character or not transliteration:
        return True
    if len(character) > 20 or len(transliteration) > 20:
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
        return True
    if len(word) > 50 or len(translation) > 50:
        return False
    sql = text("""INSERT INTO words (word, translation, course_id)
                  VALUES (:word, :translation, :course_id)""")
    db.session.execute(sql, {"word":word, "translation":translation, "course_id":course_id})
    db.session.commit()
    return True

def add_material(material, course_id):
    if not material:
        return False
    if len(material) > 6000:
        return False
    sql = text("""INSERT INTO course_material (material, course_id)
                  VALUES (:material, :course_id)""")
    db.session.execute(sql, {"material":material, "course_id":course_id})
    db.session.commit()
    return True


def course_id(name):
    sql = text("SELECT id FROM courses WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    course_id = result.fetchone()
    if course_id is not None:
        return course_id[0]

def encode_parameter(course_name): #the name of the course is made suitable for an url
    return urllib.parse.quote(course_name)

def decode_url(url_course_name): #returns the real name of a course
    return urllib.parse.unquote(url_course_name)

def course_teacher(name):
    sql = text("SELECT teacher FROM courses WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    teacher = result.fetchone()
    if teacher is not None:
        return teacher[0]


def return_courses():
    sql = text("SELECT name, teacher, description, url_name FROM courses")
    result = db.session.execute(sql)
    courses = result.fetchall()
    if courses is not None:
        return courses

def return_own_courses(teacher):
    sql = text("SELECT name, url_name FROM courses WHERE teacher=:teacher")
    result = db.session.execute(sql, {"teacher":teacher})
    courses = result.fetchall()
    return courses

def return_course_words(course_id):
    sql = text("SELECT word, translation, id FROM words WHERE course_id=:course_id")
    result = db.session.execute(sql, {"course_id":course_id})
    words = result.fetchall()
    return words

def return_course_characters(course_id):
    sql = text("SELECT character, transliteration, id FROM characters WHERE course_id=:course_id")
    result = db.session.execute(sql, {"course_id":course_id})
    characters = result.fetchall()
    return characters

def return_course_material(course_id):
    sql = text("SELECT id, material FROM course_material WHERE course_id=:course_id")
    result = db.session.execute(sql, {"course_id":course_id})
    material = result.fetchall()
    return material

def enroll(user_id, course_id): #user is enrolled in a course
    try:
        sql = text("""INSERT INTO enrollments (user_id, course_id)
                      VALUES (:user_id, :course_id)""")
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
        db.session.commit()
    except:
        return

def return_enrolled_courses(user_id): #returns the courses the user is enrolled in
    sql = text("""SELECT c.name, c.teacher, c.description, c.url_name
                  FROM courses c JOIN enrollments e ON c.id=e.course_id
                  WHERE e.user_id=:user_id""")
    result = db.session.execute(sql, {"user_id":user_id})
    enrolled_courses = result.fetchall()
    return enrolled_courses

def return_answers(questions, input_answers, correct_answers): #makes a list with lists that have the character or word in question, the user's answer,
        answer_list = []                                       #the correct answer and 1 or 0 depending on whether the answer was correct or not
        for i in range(0, len(questions)):
            result = check_answer(input_answers[i], correct_answers[i])
            answer_list.append([questions[i], input_answers[i], correct_answers[i], result])
        return answer_list

def check_answer(input_answer, correct_answer):
    if input_answer == correct_answer:
        return 1
    else:
        return 0

def exercise_passed(answer_list, course_id, user_id, exercise_number): #if all answers are correct, the exercise from the course is passed
    for answer in answer_list: #check all answers
        if answer[3] != 1:
            return
    if exercise_number == "1": #exercise 1 is passed
        try:
            sql = text("UPDATE enrollments SET exercise1 = 1 WHERE course_id=:course_id AND user_id=:user_id")
            db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
            db.session.commit()
        except:
            return
    if exercise_number == "2": #exercise 2 is passed
        try:
            sql = text("UPDATE enrollments SET exercise2 = 1 WHERE course_id=:course_id AND user_id=:user_id")
            db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
            db.session.commit()
        except:
            return


def delete_course(course_id):
    sql = text("DELETE FROM courses WHERE id=:course_id")
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()

def delete_material(material_id):
    sql = text("DELETE FROM course_material WHERE id=:material_id")
    db.session.execute(sql, {"material_id":material_id})
    db.session.commit()


def delete_character(character_id):
    sql = text("DELETE FROM characters WHERE id=:character_id")
    db.session.execute(sql, {"character_id":character_id})
    db.session.commit()


def delete_word(word_id):
    sql = text("DELETE FROM words WHERE id=:word_id")
    db.session.execute(sql, {"word_id":word_id})
    db.session.commit()
