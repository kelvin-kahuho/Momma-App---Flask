from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__, static_url_path='/index', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '788d5501a3787d2ddfe537f2f40239f3'

from index.models import User, Appointment, Doctor, Timeslot
admin = Admin(app, name='Admin Interface')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Appointment, db.session))

from index import routes
