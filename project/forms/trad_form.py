from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms.fields import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CreateTradForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    preview = StringField("Превью (макс. 70 слов)", validators=[DataRequired()])
    content = TextAreaField("Содержание статьи", validators=[DataRequired()])
    photo = FileField("Обложка обсуждения (необязательно)")
    is_private = BooleanField("Сделать приватным?")
    submit = SubmitField("Создать")
