from forms import db
from werkzeug.security import generate_password_hash, check_password_hash

users_committees_table = db.Table('users_committees',
    db.Column('user', db.Integer, db.ForeignKey('user.id')),
    db.Column('committee', db.Integer, db.ForeignKey('committee.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(40))
    email = db.Column(db.String(255), unique=True)
    committees = db.relationship('Committee', secondary=users_committees_table,
        backref=db.backref('members', lazy='dynamic'))

    def __init__(self, name, password, email):
        self.name = name
        self.set_password(password)
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Committee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    rights = db.Column(db.Integer)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    description = db.Column(db.String())
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime(), nullable=True)
    location = db.Column(db.String(80))
  

class Form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    deadline = db.Column(db.DateTime())
    fields = db.relationship('Field', backref='form',
                              lazy='dynamic')
    entries = db.relationship('Entry', backref='form',
                               lazy='dynamic')


class Field(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    label = db.Column(db.String(80))
    data_type = db.Column(db.Integer)
    required = db.Column(db.Boolean)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    values = db.relationship('EntryValue')

class EntryValue(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    field = db.Column(db.Integer, db.ForeignKey('Field.id'))
    value = db.Column(db.String)
