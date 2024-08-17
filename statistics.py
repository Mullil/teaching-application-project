from db import db
from flask import session
from sqlalchemy.sql import text

def return_user_stats(user_id): #returns the courses a user is enrolled in and the number of exercises completed (null is handled as zero)
    sql = text("""SELECT c.name, COALESCE(e.exercise1, 0) + COALESCE(e.exercise2, 0)
                      FROM courses c JOIN enrollments e ON c.id=e.course_id WHERE e.user_id=:user_id""")
    result = db.session.execute(sql, {"user_id":user_id})
    user_stats = result.fetchall()
    return user_stats


def return_course_stats(course_id):
    try:
        sql = text("""SELECT u.username, COALESCE(e.exercise1, 0) + COALESCE(e.exercise2, 0)
                      FROM enrollments e JOIN users u ON e.user_id=u.id WHERE e.course_id=:course_id""")
        result = db.session.execute(sql, {"course_id":course_id})
        course_stats = result.fetchall()
        return course_stats
    except:
        return
                      
