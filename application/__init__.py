from flask import Flask
from flask_bootstrap import Bootstrap
from application.extensions import create_db

application = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)
db = create_db(application)

from . import views

