from forms import db
from forms.models import User, Committee, Activity, Form, Field
from datetime import datetime

# Create the database
db.create_all()

# Create some users
u_martijn = User('Martijn', 'test', 'martijn@svcover.nl')
c_admin = Committee('admin', True)

db.session.add(u_martijn)
db.session.add(c_admin)
db.session.commit()

u_martijn.committees.append(c_admin)
db.session.commit()

activity1 = Activity('Activity1', 'test', c_admin.id, 'Groningen', datetime.utcnow())

db.session.add(activity1)
db.session.commit()

form1 = Form(activity1.id)

db.session.add(form1)
db.session.commit()

field1 = Field(form1.id, 'Field1', 0, 0)
field2 = Field(form1.id, 'Field2', 1, 0)

db.session.add(field1)
db.session.add(field2)
db.session.commit()