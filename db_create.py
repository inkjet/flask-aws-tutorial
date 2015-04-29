from application import db
from application.models import Data

db.create_all()

print("DB created.")
