from config import Configuretion

from flask import Flask, render_template, flash, request
from forms import UserForm, PostForm 
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Configuretion)
app.config['SECRET_KEY'] = 'qazzaq'
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route("/")
def index():
   return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html') 


# def users

@app.route('/user/add', methods=['GET','POST'], )
def add_user():
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

    return render_template('add_user.html', form=form, name=name, all_users=Users.query.all() )

@app.route('/user/update/<int:id>', methods=['GET','POST'])
def update_user(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.username = form.username.data       
        user_to_update.email = form.email.data 
        try:
            db.session.commit()
            flash("User updadet succesfully")
            return render_template('update_user.html', form=form, user_to_update=user_to_update,  all_users=Users.query.all() )
        except:
            flash("User updadet error")
            return render_template('update_user.html', form=form, user_to_update=user_to_update,  all_users=Users.query.all() )
    else:
        return render_template('update_user.html', name=user_to_update.username, form=form, user_to_update=user_to_update,  all_users=Users.query.all() )

@app.route('/user/<int:id>')
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


# def post

@app.route('/posts/add_post', methods=['GET', 'POST'])
def add_post():
    post_slug = None
    form = PostForm()
    if form.validate_on_submit():
        post_slug = Post.query.filter_by(slug=form.slug.data).first()
        if post_slug is None:
            post = Post(slug=form.slug.data, title=form.title.data, body=form.body.data)
            db.session.add(post)
            db.session.commit()
            flash('Post added succefully')

            # Clear the form
            form.slug.data = ''
            form.title.data = ''
            form.body.data = ''
        else:
            flash('This slug is in database. Write another Slug')

    return render_template('add_post.html', form=form, all_posts=Post.query.all())

@app.route('/posts/delete/<int:id>')
def postdelete(id):
    name = None
    form = PostForm()
    post_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_delete)
        db.session.commit()
        flash("post deleted")
        return render_template('add_post.html', form=form, name=name, all_posts=Post.query.all())
    except:
        flash('error')
        return render_template('add_post.html', form=form, name=name)


# db_class

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # create a String
    def __repr__(self): 
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title
