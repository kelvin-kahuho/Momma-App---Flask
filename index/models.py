from enum import unique
from index import db
from datetime import date, datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    specialty = db.Column(db.String(120), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return '<Doctor %r>' % self.name

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return '<Appointment %r>' % self.id