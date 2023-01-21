from flask import render_template, request, session, redirect, url_for
from index import app, admin, db
from index.models import User, Appointment


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # validate input
        if not username or not email or not password:
            error = "All fields are required"
            return render_template("signup.html", error=error)
        # check if user exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            error = "Username or email already exists"
            return render_template("signup.html", error=error)
        # create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["logged_in"] = True
        session["username"] = new_user.username
        return redirect(url_for("home"))
    else:
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
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
            error = "Invalid username or password"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


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



