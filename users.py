from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets
import re


def login(username, password):
    try:
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
    except:
        return False



def register(username, password, password_again):
    if password != password_again:
        return False
    if len username > 25 or len(password > 100):
        return False
    try:
        if not re.match("^[a-zA-Z0-9äöÄÖ]+$", username):
            return False
        hash_value = generate_password_hash(password)
        sql1 = text("INSERT INTO usernames (username) VALUES (:username)")
        sql2 = text("INSERT INTO users (username, password) VALUES (:username,:password)")
        db.session.execute(sql1, {"username":username})
        db.session.execute(sql2, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id",0)
