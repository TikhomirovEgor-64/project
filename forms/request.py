from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SendRequest(FlaskForm):
    search = StringField('Введите фамилию, имя или отчество пользователя, которому хотите отправить запрос на добавление в друзья', validators=[DataRequired()])
    submit = SubmitField('Поиск')
