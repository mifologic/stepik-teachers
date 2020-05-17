import json

from data import goals, teachers

add_goals = goals
add_teachers = teachers

days = {"mon": "Понедельник", "tue": "", "wed": "Среда", "thu": "Четверг", "fri": "Пятница", "sat": "Суббота",
        "sun": "Воскресенье"}

with open("goals.json", "w") as f:
    json.dump(add_goals, f, ensure_ascii=False)

with open("teachers.json", "w") as f:
    json.dump(add_teachers, f, ensure_ascii=False, indent=2)

with open("days.json", "w") as f:
    json.dump(days, f, ensure_ascii=False)
