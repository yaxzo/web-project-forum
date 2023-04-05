from flask_wtf import FlaskForm

from wtforms.fields import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
