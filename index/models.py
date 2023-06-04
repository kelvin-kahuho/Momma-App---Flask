from enum import unique
from index import db
from datetime import date, datetime, time


#User's class/ patient
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

#Doctors class
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    time_slots = db.relationship('Timeslot', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return '<Doctor %r>' % self.name
    
#Appointment class
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id'), nullable=False)
    timeslot = db.relationship('Timeslot', backref='appointments')

 
    def __repr__(self):
        return '<Appointment %r>' % self.name
    
#Timeslots class
class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_booked = db.Column(db.Boolean, default=False)

#Class message - stores users chats with the chatbot- this class will be implemented later    
"""
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_input = db.Column(db.String(255))
    bot_response = db.Column(db.String(1000))

    def __repr__(self):
        return '<Message %r>' % self.id
    
"""