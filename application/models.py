from application import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(128), index=True, unique=False)
    greeting = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, notes, greeting):
        self.notes = notes
        self.greeting = greeting

    def __repr__(self):
        return '<Data %r>' % self.notes