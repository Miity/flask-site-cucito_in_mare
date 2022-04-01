from app import db, app
from datetime import datetime
import os
from slugify import slugify

from flask_security import UserMixin, RoleMixin


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

    def __repr__(self):
        return '<Role %r>' % self.name


class Post(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(80), nullable=False)
    short_desc = db.Column(db.String(250), nullable=True)
    body = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    thumbnail = db.Column(db.String(80), nullable=True)

    def path_to_save(self):
        path = str(os.path.join('static', 'upload', 'posts', str(self.slug)))
        return path

    def generate_slug(self):
        self.slug = slugify(self.title)

    def path_to_thumbnail(self):
        path = str(os.path.join(
            app.config['UPLOAD_FOLDER'], 'posts', str(self.slug)))
        path = str(os.path.join(path, self.thumbnail))
        return path

    def __repr__(self):
        return '<Post %r>' % self.title

    def __init__(self, **kwargs):
        kwargs['slug'] = slugify(kwargs.get('title'))
        super(Post, self).__init__(**kwargs)
