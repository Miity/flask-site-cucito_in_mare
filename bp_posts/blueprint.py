from flask import Blueprint, render_template, flash, request, redirect, url_for
from .forms import PostForm
from models import Post
from flask_security import login_required
from flask_ckeditor import upload_success, upload_fail


from app import db


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts_admin/index.html', posts=posts)


@posts.route('/<slug>')
def detail_post(slug):
    post = Post.query.filter(Post.slug == str(slug)).first()
    return render_template('posts_admin/detail_post.html', post=post)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post_slug = Post.query.filter_by(slug=form.slug.data).first()
        if post_slug is None:
            post = Post(slug=form.slug.data,
                        title=form.title.data, body=form.body.data)
            db.session.add(post)
            db.session.commit()
            flash('Post added succefully')

            # Clear the form
            form.slug.data = ''
            form.title.data = ''
            form.body.data = ''
        else:
            flash('This slug is in database. Write another Slug')
    return render_template(
        'posts_admin/create_post.html',
        form=form,
        posts=Post.query.all())


@posts.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter(Post.id == id).first()
    form = PostForm(obj=post)

    if request.method == "POST":
        # наполнение данными request.form в obj=post
        form = PostForm(request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.index', all_posts=Post.query.all()))

    return render_template('posts_admin/edit_post.html', post=post, form=form, posts=Post.query.all())


@posts.route('/<int:id>/delete')
@login_required
def delete_post(id):
    form = PostForm()
    post_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_delete)
        db.session.commit()
        flash("post deleted")
        return redirect(url_for(
            'posts.index',
            posts=Post.query.all())
        )

    except:
        flash('error')
        return redirect(url_for(
            'posts.index',
            posts=Post.query.all())
        )


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/upload/images/'
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('/upload/images/', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)
