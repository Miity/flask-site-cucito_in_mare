from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[Email()])
    roles = StringField('Email', validators=[Email()])
    submit = SubmitField('Submit')
