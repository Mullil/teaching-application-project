from app import app
from flask import session, render_template, request, redirect
import users, teachers, courses, statistics
import random

@app.route("/")
def index():
    user_id = users.user_id()
    my_courses = courses.return_enrolled_courses(user_id)
    return render_template("index.html", my_courses = my_courses)


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = "Väärä käyttäjätunnus tai salasana!"
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.login(username, password):
            return redirect("/")
        if teachers.login(username, password):
            return redirect("/teacher")
        else:
            return render_template("login.html", error_message = error_message, username = username, password = password)

@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = "Rekisteröityminen epäonnistui!"
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        teacher = "teacher" in request.form
        if teacher and teachers.register(username, password, password_again):
            return redirect("/teacher")
        if users.register(username, password, password_again):
            return redirect("/")
        else:
            return render_template("register.html", error_message = error_message, username = username, password = password, password_again = password_again)


@app.route("/logout")
def logout():
    try:
        users.logout()
    except:
        teachers.logout()
    return redirect("/")

@app.route("/teacher")
def teacher_view():
    teacher_id = teachers.teacher_id()
    teacher_name = teachers.teacher_name(teacher_id)
    own_courses = courses.return_own_courses(teacher_name)
    return render_template("teacher.html", teacher_name = teacher_name, own_courses = own_courses)


@app.route("/teacher/<teacher_name>/createcourse", methods=["GET", "POST"])
def create_course(teacher_name):
    if request.method == "GET":
        return render_template("createcourse.html", teacher_name=teacher_name)
    if request.method == "POST":
        course_name = request.form.get("course_name")
        course_description = request.form.get("course_description")
        url_course_name = courses.encode_parameter(course_name)
        if courses.create_course(course_name, teacher_name, course_description):
            return redirect(f"/editcourse/{url_course_name}")

@app.route("/editcourse/<url_course_name>", methods=["GET", "POST"])
def edit_course(url_course_name):
    course_name = courses.decode_url(url_course_name)
    course_id = courses.course_id(course_name)
    course_characters = courses.return_course_characters(course_id)
    course_words = courses.return_course_words(course_id)
    url_course_name = courses.encode_parameter(course_name)
    if request.method == "GET":
        return render_template("editcourse.html", url_course_name = url_course_name, course_name = course_name, course_characters = course_characters, course_words = course_words)
    if request.method == "POST":        
        character = request.form.get("character")
        transliteration = request.form.get("character_transliteration")
        word = request.form.get("word")
        translation = request.form.get("word_translation")
        courses.add_characters(character, transliteration, course_id)
        courses.add_words(word, translation, course_id)
        return redirect(f"/editcourse/{url_course_name}")




@app.route("/coursematerial/<url_course_name>", methods=["GET", "POST"])
def add_course_material(url_course_name):
    course_name = courses.decode_url(url_course_name)
    url_course_name = courses.encode_parameter(course_name)
    if request.method == "GET":
        return render_template("coursematerial.html", url_course_name = url_course_name, course_name = course_name)
    if request.method == "POST":
        course_material = request.form.get("course_material")
        course_id = courses.course_id(course_name)
        if courses.add_material(course_material, course_id):
            return redirect("/teacher")

@app.route("/courses", methods=["GET"])
def all_courses():
    course_info = courses.return_courses()
    if request.method == "GET":
        return render_template("courses.html", course_info = course_info)

@app.route("/exercises/<url_course_name>", methods=["GET"])
def exercises(url_course_name):
    course_name = courses.decode_url(url_course_name)
    course_id = courses.course_id(course_name)
    course_material = courses.return_course_material(course_id)
    if request.method == "GET":
        user_id = users.user_id()
        courses.enroll(user_id, course_id)
        return render_template("exercises.html", url_course_name = url_course_name, course_name = course_name, course_material = course_material)

@app.route("/exercises/1/<url_course_name>", methods=["GET"])
def exercise1(url_course_name):
    course_name = courses.decode_url(url_course_name)
    url_course_name = courses.encode_parameter(course_name)
    course_id = courses.course_id(course_name)
    characters = courses.return_course_characters(course_id)
    random.shuffle(characters)
    if request.method == "GET":
        return render_template("exercise1.html", course_name = course_name, url_course_name = url_course_name, characters = characters)

@app.route("/exercises/2/<url_course_name>", methods=["GET"])
def exercise2(url_course_name):
    course_name = courses.decode_url(url_course_name)
    url_course_name = courses.encode_parameter(course_name)
    course_id = courses.course_id(course_name)
    words = courses.return_course_words(course_id)
    random.shuffle(words)
    if request.method == "GET":
        return render_template("exercise2.html", course_name = course_name, url_course_name = url_course_name, words = words)

@app.route("/answers/<url_course_name>", methods=["POST"]) #answers route shows the users answers to exercises with correct answers and points given
def answers(url_course_name):
    course_name = courses.decode_url(url_course_name)
    url_course_name = courses.encode_parameter(course_name)
    course_id = courses.course_id(course_name)
    if request.method == "POST":
        exercise_number = request.form.get("exercise")
        questions = request.form.getlist("question") #questions are the words or characters in an exercise
        input_answers = request.form.getlist("answer")
        correct_answers = request.form.getlist("correct_answer")
        answers = courses.return_answers(questions, input_answers, correct_answers)
        user_id = users.user_id()
        courses.exercise_passed(answers, course_id, user_id, exercise_number)
        return render_template("answers.html", course_name = course_name, url_course_name = url_course_name, answers = answers)

@app.route("/userstatistics", methods=["GET"])
def user_statistics():
    if request.method == "GET":
        user_id = users.user_id()
        user_stats = statistics.return_user_stats(user_id)
        return render_template("user_stats.html", user_stats = user_stats)

@app.route("/statistics/<url_course_name>", methods=["GET"])
def course_statistics(url_course_name):
    course_name = courses.decode_url(url_course_name)
    course_id = courses.course_id(course_name)
    course_stats = statistics.return_course_stats(course_id)
    if request.method == "GET":
        return render_template("course_stats.html", course_stats = course_stats)


@app.route("/deletecourse/<url_course_name>", methods=["GET"])
def delete_course(url_course_name):
    course_name = courses.decode_url(url_course_name)
    course_id = courses.course_id(course_name)
    if request.method == "GET":
        courses.delete_course(course_id)
        return redirect("/teacher")

