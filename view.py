from app import app
from flask import render_template, request, url_for, send_from_directory
from forms import SiteForm
from models import Users
from flask_security import login_required
from models import Post, Tag, Image
import os
from utils import save_img


@app.route("/")
def index():
    tags = Tag.query.filter_by(archive=False).all()
    posts = Post.query.filter_by(archive=False).all()
    images = Image.query.filter_by(archive=False).all()
    return render_template("blog/index.html", all_posts=posts, tags=tags, images=images)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')


@app.errorhandler(405)
def page_not_found_405(error):
    return render_template('page_not_found.html')


# Admin

@app.route('/users')
@login_required
def all_users():
    users = Users.query.all()
    return render_template('users/users.html', users=users)


@app.route('/admin/site_set', methods=['GET', 'POST'])
def site_set():
    form = SiteForm()
    if form.validate_on_submit() and form.logo.data:
        path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], 'main_set')
        save_img(form.logo.data, path_to_save, 'logo.jpg')
    return render_template('blog/site_set.html', form=form)


@app.route('/upload/posts/<path:slug>/<path:filename>')
def download_post_image(slug, filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', slug)
    return send_from_directory(path, filename, as_attachment=True)


# Utils
from flask_ckeditor import upload_success, upload_fail


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'ckeditor')
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'ckeditor', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    # return upload_success call
    return upload_success(url, filename=f.filename)
