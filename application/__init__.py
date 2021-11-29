from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)

from . import views

db = SQLAlchemy(application)
db.create_all()