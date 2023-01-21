from flask import render_template, flash, redirect, url_for
from index import app, admin
from index.models import User, Appointment

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def log_in():

    return render_template("login.html")

@app.route("/book", methods=['GET', 'POST'])
def book_appointment():
    return render_template("book_appointment.html")

@app.route("/view")
def view_appointment():
    return render_template("view_appointments.html")

@app.route("/profile")
def view_profile():
    return render_template("profile.html")

@app.route('/admin')
def admin_panel():
    return render_template('admin.html', admin=admin)



