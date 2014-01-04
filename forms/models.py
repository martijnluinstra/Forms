from forms import db
from datetime import datetime
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
    admin = db.Column(db.Boolean)

    def __init__(self, name, admin=False):
        self.name = name
        self.admin = admin


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    description = db.Column(db.String)
    committee_id = db.Column(db.Integer, db.ForeignKey('committee.id'))
    location = db.Column(db.String(80))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, description, committee_id, location, start_time, end_time=None):
        self.name = name
        self.description = description
        self.committee_id = committee_id
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
  

class Form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    deadline = db.Column(db.DateTime, nullable=True)
    fields = db.relationship('Field', backref='form',
                              lazy='dynamic')
    entries = db.relationship('Entry', backref='form',
                               lazy='dynamic')

    def __init__(self, activity_id, deadline=None):
        self.activity_id = activity_id
        self.deadline = deadline


class Field(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    label = db.Column(db.String(80))
    display_index = db.Column(db.Integer)
    data_type = db.Column(db.Integer)
    required = db.Column(db.Boolean)
    __table_args__ = (db.UniqueConstraint('form_id', 'display_index'),
        )

    def __init__(self, form_id, label, display_index, data_type, required=True):
        self.form_id = form_id
        self.label = label
        self.display_index = display_index
        self.data_type = data_type
        self.required = required


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    timestamp = db.Column(db.DateTime)
    values = db.relationship('EntryValue')

    def __init__(self, form_id):
        self.form_id = form_id
        self.timestamp = datetime.utcnow()


class EntryValue(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))
    value = db.Column(db.String)

    def __init__(self, field, value, entry):
        self.entry = entry_id
        self.field = field_id
        self.value = value