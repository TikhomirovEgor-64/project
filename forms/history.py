from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField


class AddHistory(FlaskForm):
    image = FileField('Изображение истории')
    text = StringField('Расскажите вашу историю')
    submit = SubmitField('Добавить историю')
