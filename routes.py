from app import app
from flask import session, render_template, request, redirect
import users, teachers, courses

@app.route("/")
def index():
    user_id = users.user_id()
    my_courses = courses.return_enrolled_courses(user_id)
    return render_template("index.html", my_courses = my_courses)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.login(username, password):
            return redirect("/")
        if teachers.login(username, password):
            return redirect("/teacher")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        teacher = "teacher" in request.form
        if teacher and teachers.register(username, password):
            return redirect("/teacher")
        if users.register(username, password):
            return redirect("/")


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










