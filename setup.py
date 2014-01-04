from forms import db
from forms.models import User, Committee

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