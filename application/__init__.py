from flask import Flask
from flask_bootstrap import Bootstrap
from application.extensions import db
from . import models

application = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)
db.init_app(application)

with application.app_context():
    db.create_all()

from . import views

