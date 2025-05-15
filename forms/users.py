from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта *', validators=[DataRequired()])
    password = PasswordField('Пароль *', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль *', validators=[DataRequired()])
    name = StringField('Имя пользователя *', validators=[DataRequired()])
    surname1 = StringField('Фамилия пользователя')
    surname2 = StringField('Отчество пользователя')
    date_of_birth = DateField('Дата рождения *', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
