import json
from app import db, Teacher

from data import goals, teachers

add_goals = goals
add_teachers = teachers


# db.create_all()

for t in teachers:
    teacher = Teacher(name=t["name"], about=t["about"], rating=t["rating"], picture=t["picture"],
                      price=t["price"], goals=json.dumps(t["goals"]), free_time=json.dumps(t["free"]))
    db.session.add(teacher)
db.session.commit()
