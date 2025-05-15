from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class Chat(FlaskForm):
    text = StringField('Написать сообщение')
    submit = SubmitField('Отправить')
