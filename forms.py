from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    slug = StringField('Slug')
    title = StringField('Title')
    body = StringField('Body Text', widget=TextArea())
    submit = SubmitField('Submit')