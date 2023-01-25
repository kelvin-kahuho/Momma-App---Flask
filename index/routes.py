from flask import render_template, request, session, redirect, url_for
from index import app, admin, db
from index.models import User, Appointment



@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # validate input
        if not username or not email or not password:
            error = "All fields are required!"
            return render_template("signup.html", error=error)
        # check if user exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            error = "Username or email already exists!"
            return render_template("register.html", error=error)
        # create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["logged_in"] = True
        session["username"] = new_user.username
        return redirect(url_for("home"))
    else:
        return render_template("register.html")

@app.route("/", methods=['GET', 'POST'])
def log_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #check if user exist
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["logged_in"] = True
            session["username"] = user.username
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password!"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("log_in"))


#Function to check if user is logged in

def check_authentication():
    if not session.get("logged_in"):
        return redirect(url_for("log_in"))


@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/book", methods=['GET', 'POST'])
def book_appointment():
    check_authentication()
    if request.method == 'POST':        
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']
        username = session['username']
        user = User.query.filter_by(username=username).first()
        appointment = Appointment(name=name, email=email, date=date, time=time, message=message, user_id=user.id)

        try:
            db.session.add(appointment)
            db.session.commit()
            success = 'Appointment booked successfully!'
            return render_template("book_appointment.html", success=success)
        except:
            error = 'There was an issue booking your appointment'
            return render_template("book_appointment.html", error=error)

    else:
        return render_template("book_appointment.html")

@app.route("/view")
def view_appointment():
    check_authentication()
    username = session['username']
    user = User.query.filter_by(username=username).first()
    appointments = Appointment.query.filter_by(user_id=user.id)
    return render_template("view_appointments.html", appointments=appointments)

@app.route("/profile")
def view_profile():
    check_authentication()
    username = session['username']
    user = User.query.filter_by(username=username).first()
    appointments = Appointment.query.filter_by(user_id=user.id)
    return render_template("profile.html", user=user, appointments=appointments)

@app.route('/admin')
def admin_panel():
    return render_template('admin.html', admin=admin)



