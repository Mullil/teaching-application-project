from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import re

def login(username, password):
    sql = text("SELECT id, password FROM teachers WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    teacher = result.fetchone()
    if not teacher:
        return False
    if check_password_hash(teacher.password, password):
        session["teacher_id"] = teacher.id
        return True
    return False



def register(username, password):
    hash_value = generate_password_hash(password)
    if not re.match("^[a-zA-Z0-9äöÄÖ]+$", username):
        return False
    try:
        sql1 = text("INSERT INTO usernames (username) VALUES (:username)")
        sql2 = text("INSERT INTO teachers (username, password) VALUES (:username,:password)")
        db.session.execute(sql1, {"username":username})
        db.session.execute(sql2, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["teacher_id"]

def teacher_id():
    return session.get("teacher_id",0)

def teacher_name(teacher_id):
    sql = text("SELECT username FROM teachers WHERE id=:teacher_id")
    result = db.session.execute(sql, {"teacher_id":teacher_id})
    name = result.fetchone()
    return name[0]


