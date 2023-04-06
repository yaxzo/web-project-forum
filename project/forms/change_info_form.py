from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    username = StringField("Новое имя пользователя")
    email = EmailField("Новая почта пользователя")
    photo = FileField("Новое фото профиля")
    password = PasswordField("Введите пароль от своего аккаунта", validators=[DataRequired()])
    submit = SubmitField("Обновить данные")
