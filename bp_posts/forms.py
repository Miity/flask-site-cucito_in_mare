from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileRequired


class PostForm(FlaskForm):
    slug = StringField('Slug')
    title = StringField('Title')
    short_desc = StringField('short_desc', widget=TextArea())
    body = CKEditorField('Body', widget=TextArea())
    thumbnail = FileField('Thumbnail',validators=[FileRequired()])
    submit = SubmitField('Submit')
