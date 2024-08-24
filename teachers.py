from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets
import re

def login(username, password):
    try:
        sql = text("SELECT id, password FROM teachers WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        teacher = result.fetchone()
        if check_password_hash(teacher.password, password):
            session["teacher_id"] = teacher.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
    except:
        return False



def register(username, password, password_again):
    if password != password_again:
        return False
    try:
        if not re.match("^[a-zA-Z0-9äöÄÖ]+$", username):
            return False
        hash_value = generate_password_hash(password)
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


