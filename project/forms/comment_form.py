from flask_wtf import FlaskForm

from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment_text = TextAreaField("", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")
