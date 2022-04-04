from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField


class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[Email()])
    roles = StringField('Email', validators=[Email()])
    submit = SubmitField('Submit')