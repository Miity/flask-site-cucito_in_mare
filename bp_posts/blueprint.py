from flask import Blueprint, render_template, flash, request, redirect, url_for, send_from_directory
from .forms import PostForm, TagForm, ImageForm
from models import Post, Tag, Image
from flask_security import login_required
from werkzeug.utils import secure_filename
import os
from slugify import slugify
from utils import save_img


from app import app, db

posts = Blueprint('posts', __name__, template_folder='templates')


def redirect_to_index():
    return redirect(url_for(
        'posts.index',
        posts=Post.query.all(),
        tags=Tag.query.all())
    )


def post_update(post, form):
    tag = Tag.query.filter_by(name=form.tags.data)
    post.title = form.title.data
    post.body = form.body.data
    post.short_desc = form.short_desc.data
    post.tags = list(tag)
    post.video_url = form.video_url.data
    return post


@posts.route('/')
def index():
    return render_template('posts_admin/index.html',
                           posts=Post.query.all(),
                           tags=Tag.query.all()
                           )


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post_slug = Post.query.filter_by(slug=slugify(form.title.data)).first()
        if post_slug is None:
            post = Post(title=form.title.data)
            post = post_update(post, form)
            # SAVE FILE
            if form.thumbnail.data:
                filename = secure_filename(form.thumbnail.data.filename)
                post.thumbnail = filename
                save_img(form.thumbnail.data, post.path_to_save())
                flash('Image added')
            db.session.add(post)
            db.session.commit()
            flash('Post added succefully')
            return redirect_to_index()
        else:
            flash('This slug is in database. Write another Slug')
    return render_template('/posts_admin/create_post.html', form=form)


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
            os.system("rm -r static/upload/posts/" + post_delete.slug)
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
    if tag_delete.archive:
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


# Image
@posts.route('/images')
def all_images():
    return render_template('posts_admin/index_images.html',
                           images=Image.query.all())


@posts.route('/create_image', methods=['GET', 'POST'])
@login_required
def create_image():
    form = ImageForm()
    if form.validate_on_submit():
        tag = Tag.query.filter_by(name=form.tags.data)
        image = Image(alt=form.alt.data, tags=list(tag))
        # SAVE FILE
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image.name = filename
            save_img(form.image.data, image.path_to_save())
            flash('Image added')
        db.session.add(image)
        db.session.commit()
        return redirect_to_index()
    return render_template('posts_admin/create_image.html', form=form)


@posts.route('/images/<path:filename>')
def download_image(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
    return send_from_directory(path, filename, as_attachment=True)


@posts.route('/image_<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_image(id):
    image = Image.query.get(id)
    if request.method == "POST":
        form = ImageForm(obj=image)
        if form.validate_on_submit():
            tag = Tag.query.filter_by(name=form.tags.data)
            image = Image(alt=form.alt.data, tags=list(tag))
            db.session.commit()
            flash('Image updated succefully')
        return redirect_to_index()
    form = ImageForm(obj=image)
    return render_template('posts_admin/create_image.html',
                           form=form,
                           )


@posts.route('/image_<int:id>/delete')
@login_required
def delete_image(id):
    image_del = Image.query.get_or_404(id)
    if image_del.archive:
        os.system("rm static/upload/images/" + image_del.name)
        db.session.delete(image_del)
        db.session.commit()
        flash("image deleted")
        return redirect(url_for('posts.all_images', images=Image.query.all()))
    else:
        image_del.archive = True
        db.session.commit()
        return redirect(url_for('posts.all_images', images=Image.query.all()))


@posts.route('/publish_image/<int:id>')
@login_required
def publish_image(id):
    image = Image.query.get_or_404(id)
    image.archive = False
    db.session.commit()
    return redirect(url_for('posts.all_images', images=Image.query.all()))
