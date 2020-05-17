import json
import random

from flask import Flask, render_template

from forms import BookingForm, TeacherRequestForm


app = Flask("__name__")
app.secret_key = "very-secret-key"

# get teachers list
with open("teachers.json", "r") as f:
    teachers = json.load(f)


# get goals
with open("goals.json") as file:
    goals = json.load(file)


# get days
with open("days.json") as file:
    days = json.load(file)


@app.route("/")
def index():
    selected_teachers = random.sample(teachers, 6)
    return render_template("index.html", teachers=selected_teachers, goals=goals)


@app.route("/teachers/")
def show_all_teachers():
    return render_template("/teachers.html/", teachers=teachers, goals=goals)


@app.route("/goals/<goal>/")
def get_goal(goal):
    teachers_list = sorted([t for t in teachers if goal in t['goals']], key=lambda k: k['rating'], reverse=True)
    return render_template("goal.html", goals=goals, teachers=teachers_list, goal=goal)


@app.route("/profiles/<int:teacher_id>/")
def get_teacher(teacher_id):
    teacher = ""
    time = ""
    for t in teachers:
        if t["id"] == teacher_id:
            teacher = t
            time = teacher["free"]
    return render_template("profile.html", teacher=teacher, goals=goals, time=time, days=days)


@app.route("/request/")
def request():
    form = TeacherRequestForm()
    return render_template("request.html", form=form)


@app.route("/request_done/", methods=["POST"])
def request_done():
    form = TeacherRequestForm()
    goal = form.goals.data
    time = form.free_time.data
    name = form.name.data
    phone = form.phone.data

    if form.validate_on_submit():

        with open("request.json", "r") as json_file:
            request_file = json.load(json_file)

        request_data = {
            "id": len(request_file) + 1,
            "goal": goal,
            "time": time,
            "name": name,
            "phone": phone
        }

        request_file.append(request_data)
        with open("request.json", "w") as json_file:
            json.dump(request_file, json_file, ensure_ascii=False)

        return render_template("request_done.html", form=form, goal=goal, time=time, name=name, phone=phone)
    else:
        return "Ошибки в форме"


@app.route("/booking/<int:teacher_id>/<day_of_week>/<time>/")
def booking(teacher_id, day_of_week, time):
    form = BookingForm()
    day = days[day_of_week]
    teacher = [t for t in teachers if t["id"] == teacher_id]
    time = time.replace("-", ":")
    return render_template("booking.html", teacher=teacher, time=time, day=day, form=form)


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    form = BookingForm()
    name = form.name.data
    phone = form.phone.data
    day = form.day.data
    time = form.time.data
    if form.validate_on_submit():

        with open("booking.json", "r") as json_file:
            request_file = json.load(json_file)

        request_data = {
            "id": len(request_file) + 1,
            "name": name,
            "phone": phone,
            "time": time,
            "day": day
        }

        request_file.append(request_data)
        with open("booking.json", "w") as json_file:
            json.dump(request_file, json_file, ensure_ascii=False)

        return render_template("booking_done.html", form=form, name=name, phone=phone, day=day, time=time)
    else:
        return "Ошибки в форме"


app.run()
