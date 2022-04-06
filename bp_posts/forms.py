from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from models import Tag


class PostForm(FlaskForm):
    title = StringField('Title',)
    short_desc = StringField('short_desc', widget=TextArea())
    body = CKEditorField('Body', widget=TextArea())
    thumbnail = FileField('Thumbnail',)
    tags = SelectField('Tags', choices=[x.name for x in Tag.query.all()])
    submit = SubmitField('Submit')