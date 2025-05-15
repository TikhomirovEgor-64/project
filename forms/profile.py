from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class ProfileForm(FlaskForm):
    name = StringField('Имя пользователя:', validators=[DataRequired()])
    surname1 = StringField('Фамилия пользователя:')
    surname2 = StringField('Отчество пользователя:')
    photo = FileField()
    date_of_birth = DateField('Дата рождения:', format='%Y-%m-%d', validators=[DataRequired()])
    info_about = StringField('Информация о пользователе:')
    submit1 = SubmitField('Редактировать')
    submit2 = SubmitField('Сохранить')
