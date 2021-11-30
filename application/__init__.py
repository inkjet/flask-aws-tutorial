from flask import Flask
from flask_bootstrap import Bootstrap
from application.extensions import db, migrate
from . import models

# create and bootstrap the application
application = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)

# init and create the db
db.init_app(application)
migrate.init_app(application, db)

with application.app_context():
    db.create_all()

# this has to be relative or it overwrites the Flask application object/variable with the module itself
# it also has to be last because the app has to be created before the decorator in views.py can register the views.
from . import views

