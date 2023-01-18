from flask import render_template, flash, redirect, url_for
from index import app, admin
from index.models import User, Appointment
from index.forms import RegistrationForm, LogInForm, AppointmentForm

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('hello'))
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    if form.validate_on_submit():
        flash(f'Login successful. Welcome {form.email.data}!', 'success')
        return redirect(url_for('hello'))

    return render_template("login.html", form=form)

@app.route("/book", methods=['GET', 'POST'])
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        flash(f'You have successifully booked an appointment at {form.date.data}!', 'success')
        return redirect(url_for('view_appointment'))
    return render_template("book_appointment.html", form=form)

@app.route("/view")
def view_appointment():
    return render_template("view_appointments.html")

@app.route("/profile")
def view_profile():
    return render_template("profile.html")

@app.route('/admin')
def admin_panel():
    return render_template('admin.html', admin=admin)

@app.route('/static/<path>')
def send_image(path):
    return app.send_static_file(path)

