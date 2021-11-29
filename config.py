from environs import Env
from application.database import AWSPostgreSQL

env = Env()
env.read_env()

LOCAL_DATABASE_URI = 'postgresql://'+env.str("LOCAL_USER")+':'+env.str("LOCAL_PW")+'@localhost:5432/flask_db'
SQLALCHEMY_DATABASE_URI = (lambda x: LOCAL_DATABASE_URI if x else AWSPostgreSQL().uri)(env.bool("LOCAL_DEVELOPMENT"))
SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = env.str("APP_SECRET")
