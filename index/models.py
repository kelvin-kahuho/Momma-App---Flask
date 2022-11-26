from enum import unique
from index import db
from datetime import date, datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    doctors_note = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable = False, unique=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"User('{self.doctors_note}','{self.date}')"