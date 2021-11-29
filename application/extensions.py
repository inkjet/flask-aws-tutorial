from flask_sqlalchemy import SQLAlchemy


def create_db(application):
    db = SQLAlchemy(application)
    db.create_all()
    return db
