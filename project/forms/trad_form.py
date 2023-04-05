from flask_wtf import FlaskForm

from wtforms.fields import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class CreateTradForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    preview = StringField("Превью", validators=[DataRequired()])
    content = TextAreaField("Содержание статьи", validators=[DataRequired()])
    is_private = BooleanField("Сделать приватным?", validators=[DataRequired()])
