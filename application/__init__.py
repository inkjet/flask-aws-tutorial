from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

application = app = Flask(__name__)
application.config.from_object('config')
bootstrap = Bootstrap(application)
db = SQLAlchemy(application)
db.create_all()
