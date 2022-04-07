from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from app import db
from models import Tag


def tag_choises():
    return db.session.query(Tag).all()


class PostForm(FlaskForm):
    title = StringField('Title',)
    short_desc = StringField('short_desc', widget=TextArea())
    body = CKEditorField('Body', widget=TextArea())
    thumbnail = FileField('Thumbnail',)
    tags = SelectField('Tags', choices=tag_choises)
    submit = SubmitField('Submit')


class TagForm(FlaskForm):
    name = StringField('Name of tag',)
    desc = StringField('Description', widget=TextArea())
    submit = SubmitField('Submit')
