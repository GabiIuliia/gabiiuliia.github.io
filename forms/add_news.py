from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание')
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
