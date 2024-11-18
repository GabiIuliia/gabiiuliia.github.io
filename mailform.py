from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class MailForm(FlaskForm):
    username = StringField('Ваше имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = EmailField('Эл. почта', validators=[DataRequired(), Email()])
    message = StringField('Ваше сообщение', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Отправить')
