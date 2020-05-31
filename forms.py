from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, validators


# форма бронирования занятий
class BookingForm(FlaskForm):
    name = StringField("Вас зовут", [validators.InputRequired()])
    phone = StringField("Ваш телефон", [validators.InputRequired(),
                                        validators.Length(min=7, message="Номер не меньше 7 символов")])
    day = HiddenField()
    time = HiddenField()
    teacher = HiddenField()


# форма подбора преподавателей
class TeacherRequestForm(FlaskForm):
    goals = RadioField("goals", choices=[("Для путешествий", "Для путешествий"), ("Для школы", "Для школы"),
                                         ("Для работы", "Для работы"), ("Для переезда", "Для переезда"),
                                         ("Для программирования", "Для программирования")],
                       default="Для программирования")
    free_time = RadioField("free_time", choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                 ("3-5 часов в неделю", "3-5 часов в неделю"),
                                                 ("5-7 часов в неделю", "5-7 часов в неделю"),
                                                 ("7-10 часов в неделю", "7-10 часов в неделю")],
                           default="5-7 часов в неделю")
    name = StringField("Вас зовут", [validators.InputRequired()])
    phone = StringField("Ваш телефон", [validators.InputRequired()])
