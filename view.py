from app import app, db
from flask import render_template, flash, request, url_for, send_from_directory
from forms import UserForm, SiteForm
from models import Users
from flask_security import login_required
from models import Post, Tag
import os
from utils import save_img


@app.route("/")
def index():
    tags = Tag.query.filter_by(archive=False).all()
    posts = Post.query.filter_by(archive=False).all()
    return render_template("blog/index.html", all_posts=posts, tags=tags)


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

'''
@app.route('/users/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        name = form.username.data
        if user is None:
            user = Users(username=form.username.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            form.username.data = ''
            form.email.data = ''
            flash('user added succefully')
        else:
            flash('This user is in database. Write another Email')
    return render_template('users/create_user.html', form=form, name=name, all_users=Users.query.all())


@app.route('/user/<int:id>')
@login_required
def userdelete(id):
    name = None
    form = UserForm()
    user_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        flash("user deleted")
        return render_template('add_user.html', form=form, name=name, all_users=Users.query.all())
    except:
        flash('error')
        return render_template('add_user.html', form=form, name=name)
'''


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
