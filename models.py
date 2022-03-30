from app import db
from datetime import datetime
import re
import os
from slugify import slugify

from flask_security import UserMixin, RoleMixin
from flask_ckeditor import CKEditorField


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'users.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey(
                           'role.id'), primary_key=True)
                       )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # create a String

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Post(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    pic = db.Column(db.String(80), nullable=True)

    def path_to_files(self):
        path = str(os.path.join(app.config['UPLOAD_FOLDER'], 'posts', str(self.slug)))
        return path

    def path_to_pic(self):
        path = str(os.path.join(path, pic))
        return path

    def generate_slug(self):
        if self.slug:
            self.slug = slugify(self.slug)

    def __repr__(self):
        return '<Post %r>' % self.title

