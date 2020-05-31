import json
import random

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError

from forms import BookingForm, TeacherRequestForm


app = Flask("__name__")
app.secret_key = "very-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# get goals
with open("goals.json") as file:
    goals = json.load(file)


# get days
with open("days.json") as file:
    days = json.load(file)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.Text, nullable=False)
    free_time = db.Column(db.Text, nullable=False)
    booking = db.relationship("Booking", back_populates="teacher")


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher", back_populates="booking")


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)


teachers = db.session.query(Teacher).all()


@app.route("/")
def index():
    selected_teachers = random.sample(teachers, 6)
    return render_template("index.html", teachers=selected_teachers, goals=goals)


@app.route("/teachers/")
def show_all_teachers():
    return render_template("/teachers.html/", teachers=teachers, goals=goals)


@app.route("/goals/<goal>/")
def get_goal(goal):
    teachers_list = db.session.query(Teacher).filter(Teacher.goals.contains(goal)).order_by(Teacher.rating.desc())
    return render_template("goal.html", goals=goals, teachers=teachers_list, goal=goal)


@app.route("/profiles/<int:teacher_id>/")
def get_teacher(teacher_id):
    teacher = db.session.query(Teacher).filter(Teacher.id == teacher_id).first()
    time = json.loads(teacher.free_time)
    return render_template("profile.html", teacher=teacher, goals=goals, time=time, days=days)


@app.route("/request/", methods=["GET", "POST"])
def request():
    form = TeacherRequestForm()
    if form.validate_on_submit():
        goal = form.goals.data
        time = form.free_time.data
        name = form.name.data
        phone = form.phone.data

        request_data = Request(goal=goal, time=time, name=name, phone=phone)
        db.session.add(request_data)
        db.session.commit()

        return render_template("request_done.html", form=form, goal=goal, time=time, name=name, phone=phone)
    return render_template("request.html", form=form)


@app.route("/booking/<int:teacher_id>/<day_of_week>/<time>/", methods=["GET", "POST"])
def booking(teacher_id, day_of_week, time):

    day = days[day_of_week]
    teacher = db.session.query(Teacher).filter(Teacher.id == teacher_id).first()
    time = time.replace("-", ":")

    form = BookingForm()

    if form.validate_on_submit():

        name = form.name.data
        phone = form.phone.data
        day = form.day.data
        time = form.time.data
        teacher_id = form.teacher.data

        request_data = Booking(name=name, phone=phone, day=day, time=time, teacher_id=teacher_id)
        db.session.add(request_data)
        db.session.commit()
        return render_template("booking_done.html", form=form, name=name, phone=phone, day=day, time=time)
    return render_template("booking.html", teacher=teacher, time=time, day=day, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


@app.errorhandler(InternalServerError)
def page_not_found(e):
    return "Something is going wrong", 500


if __name__ == "__main__":
    app.run()
