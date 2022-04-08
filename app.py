from config import Configuration
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)


migrate = Migrate(app, db)
ckeditor = CKEditor(app)


from bp_posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/admin')


### Flask security ###

from models import Users, Role
user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)


@app.context_processor
def utility_processor():
    logo = 'logo.jpg'
    site_name = 'Tappezzeria Nautica "Cucito in Mare"'
    return dict(logo=logo, site_name=site_name)
