from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    slug = StringField('Slug')
    title = StringField('Title')
    #body = StringField('Body Text', widget=TextArea())
    body = CKEditorField('Body', widget=TextArea())
    submit = SubmitField('Submit')
