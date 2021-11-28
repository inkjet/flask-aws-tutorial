from environs import Env
from myapplication.database import AWSPostgreSQL

env = Env()
env.read_env()


# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'postgresql://'+env.str("LOCAL_USER")+':'+env.str("LOCAL_PW")+'@localhost:5432/flask_db'

SQLALCHEMY_DATABASE_URI = AWSPostgreSQL().uri

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = env.str("APP_SECRET")
