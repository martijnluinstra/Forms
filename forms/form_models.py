from flask.ext.wtf import Form
from wtforms import StringField

class BaseForm(Form):
    pass


def generate_field(field):
    return StringField(field.label)
