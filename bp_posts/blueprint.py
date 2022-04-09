from flask import Blueprint, render_template, flash, request, redirect, url_for
from .forms import PostForm, TagForm
from models import Post, Tag
from flask_security import login_required
from werkzeug.utils import secure_filename
import os
from slugify import slugify
from utils import save_img


from app import db

posts = Blueprint('posts', __name__, template_folder='templates')


def redirect_to_index():
    return redirect(url_for(
        'posts.index',
        posts=Post.query.all(), tags=Tag.query.all())
    )


@posts.route('/')
def index():
    return render_template('posts_admin/index.html',
                           posts=Post.query.all(),
                           tags=Tag.query.all())


def post_update(post, form):
    tag = Tag.query.filter_by(name=form.tags.data)
    post.title = form.title.data
    post.body = form.body.data
    post.short_desc = form.short_desc.data
    post.tags = list(tag)


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post_slug = Post.query.filter_by(slug=slugify(form.title.data)).first()
        if post_slug is None:
            post = Post()
            post_update(post, form)
            # SAVE FILE
            if form.thumbnail.data:
                filename = secure_filename(form.thumbnail.data.filename)
                post.thumbnail = filename
                save_img(form.thumbnail.data, post.path_to_save())
                flash('Image added')
            db.session.add(post)
            db.session.commit()
            flash('Post added succefully')
        else:
            flash('This slug is in database. Write another Slug')
    return redirect_to_index()


@posts.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    if request.method == "POST":
        form = PostForm(obj=post)
        if form.validate_on_submit():
            post_update(post, form)
            if form.thumbnail.data != post.thumbnail:
                save_img(form.thumbnail.data, post.path_to_save())
                filename = secure_filename(form.thumbnail.data.filename)
                post.thumbnail = filename
            db.session.commit()
            flash('Post updated succefully')
        return redirect_to_index()
    form = PostForm(obj=post)
    return render_template('posts_admin/edit_post.html',
                           post=post,
                           form=form,
                           )


@posts.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post_delete = Post.query.get_or_404(id)
    if post_delete.archive == True:
        try:
            db.session.delete(post_delete)
            db.session.commit()
            flash("post deleted")
            return redirect_to_index()

        except:
            flash('error')
            return redirect_to_index()
    else:
        post_delete.archive = True
        db.session.commit()
        return redirect_to_index()


@posts.route('/publish_post/<int:id>')
@login_required
def publish(id):
    post = Post.query.get_or_404(id)
    post.archive = False
    db.session.commit()
    return redirect_to_index()


# TAG
@posts.route('/create_tag', methods=['GET', 'POST'])
@login_required
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data, description=form.desc.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag added')
        return redirect_to_index()
    return render_template('posts_admin/create_tag.html', form=form)


@posts.route('/delete_tag/<int:id>')
@login_required
def delete_tag(id):
    tag_delete = Tag.query.get_or_404(id)
    if tag_delete.archive == True:
        try:
            db.session.delete(tag_delete)
            db.session.commit()
            flash("tag deleted")
            return redirect_to_index()

        except:
            flash('error')
            return redirect_to_index()
    else:
        tag_delete.archive = True
        db.session.commit()
        return redirect_to_index()


@posts.route('/publish_tag/<int:id>')
@login_required
def publish_tag(id):
    tag = Tag.query.get_or_404(id)
    tag.archive = False
    db.session.commit()
    return redirect_to_index()
