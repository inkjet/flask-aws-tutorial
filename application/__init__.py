from flask import Flask
from flask_bootstrap import Bootstrap


application = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)

from . import views