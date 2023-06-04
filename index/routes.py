from flask import render_template, request, session, redirect, url_for, jsonify
from index import app, admin, db
from index.models import User, Appointment, Doctor, Timeslot
import asyncio
import rasa
from rasa.core.agent import Agent
from datetime import datetime, timedelta, time, date

model_path = "index/models/20230504-170850-soft-beaker.tar.gz"
agent = Agent.load(model_path)


@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        # validate input
        if not username or not email or not password:
            error = "All fields are required!"
            return render_template("signup.html", error=error)
        
        #Check if Password and Confirm password are similar
        if password != confirm_password:
            error = "Passwords don't match"
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
    
@app.route("/doctor_register",methods=['GET', 'POST'])
def doctor_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        specialization = request.form["specialization"]
        password = request.form["password"]
        # validate input

        if not name or not email or not specialization or not password:
            error = "All fields are required!"
            return render_template("doctors_signup.html", error=error)
        # check if user exists

        if Doctor.query.filter_by(name=name).first() or Doctor.query.filter_by(email=email).first():
            error = "Username or email already exists!"
            return render_template("doctors_login.html", error=error)
        
        # create new Doctor

        new_doctor = Doctor(name=name, email=email, specialization=specialization, password=password)
        db.session.add(new_doctor)
        db.session.commit()
        # Generate timeslots for the new doctor

        doctor = Doctor.query.filter_by(name=name).first()
        generate_timeslots(doctor.id)
        session["logged_in"] = True
        session["username"] = doctor.name
        success = "Doctor's created successfully"
        #Doctors view appointments

        doctor = Doctor.query.filter_by(name=name).first()
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        return render_template('doctor_view_appointments.html', doctor=doctor, appointments=appointments, success=success)

    else:
        return render_template("doctors_signup.html")
    

#Generate timeslots for any new doctor
def generate_timeslots(doctor_id):
    # Define the start and end time for timeslots
    current_date = datetime.today().date()

    start_time = datetime.combine(current_date + timedelta(days=1), time(9, 0))

    end_date = datetime(2023, 7, 31, 17, 0, 0)

    
    # Define the duration of each timeslot
    slot_duration = timedelta(hours=2)
    
    # Generate timeslots from start_time to end_time
    while start_time <= end_date:
        if 9 <= start_time.hour < 17:
            # Create a new timeslot for the doctor
            timeslot = Timeslot(doctor_id=doctor_id, start_time=start_time, end_time=start_time + slot_duration)
                 
            # Add the timeslot to the database
            db.session.add(timeslot)
        
        # Increment current_time to the next timeslot
        start_time += slot_duration
        
    # Commit the changes to the database
    db.session.commit()
    
    
@app.route("/doctor_login", methods=['GET', 'POST'])
def doctor_login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        #check if user exist
        doctor = Doctor.query.filter_by(name=name).first()
        if doctor and doctor.password == password:
            session["logged_in"] = True
            session["username"] = doctor.name
            success = "Logged in successfully"
            appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
            timeslots = Timeslot.query.filter_by(doctor_id=doctor.id, is_booked=True).all() 
            return render_template('doctor_view_appointments.html', doctor=doctor, appointments=appointments, timeslots=timeslots,success=success)

        else:
            error = "Invalid username or password!"
            return render_template("doctors_login.html", error=error)
    else:
        error = "Login not successful"
        return render_template("doctors_login.html", error=error)



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
            success = "Logged in successfully"
            return render_template("chat.html", success=success)
        else:
            error = "Invalid username or password!"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    success = "Logged out successfully"
    return render_template("login.html", success=success)

#Function to check if user is logged in

def check_authentication():
    if not session.get("logged_in"):
        return redirect(url_for("log_in"))


@app.route("/home")
def home():
    return render_template("chat.html")

@app.route("/take_test", methods=['GET', 'POST'])
def take_test():
    if request.method == 'POST':

        q1 = int(request.form.get('q1'))
        q2 = int(request.form.get('q2'))
        q3 = int(request.form.get('q3'))
        q4 = int(request.form.get('q4'))
        q5 = int(request.form.get('q5'))
        q6 = int(request.form.get('q6'))
        q7 = int(request.form.get('q7'))
        q8 = int(request.form.get('q8'))
        q9 = int(request.form.get('q9'))
        q10 = int(request.form.get('q10'))

        score = round(q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10)

        if score > 13:

            score = f'Your score is, {score}/30 !'

            text = 'Mothers scoring above 12 or 13 are likely to be suffering from depression and should seek medical attention. A careful clinical evaluation by a health care professional is needed to confirm a diagnosis and establish a treatment plan'

            return render_template("book_appointment.html", score = score, text = text)
        
        else:
            
            score = f'Your score is, {score}/30 !'
            
            return render_template("chat.html", score = score)
    
    else:

        return render_template('take_test.html')
    
#Code for building the booking appointment system
#Return the booking appointment page with its dependencies like availables doctors

@app.route("/book", methods=['GET'])
def deliver_dependencies():
    available_doctors = Doctor.query.all()
    return render_template('book_appointment.html', available_doctors= available_doctors)


#Route to get the above global variables from the user

@app.route("/book_appointment", methods=['GET', 'POST'],)
def book_appointment():
    global name, email, message, doctor_id
    available_doctors = Doctor.query.all()
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        appointment_date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        doctor_id = int(request.form.get('selected_doctor'))



        if appointment_date <= datetime.now():
            error = "Selected Date is not valid."
            return render_template("book_appointment.html", error=error, available_doctors=available_doctors)
    
        else:
            # Returns all available timeslots for a particular doctor on a particular date
            timeslots = Timeslot.query.filter(
                Timeslot.doctor_id == doctor_id,
                Timeslot.start_time >= appointment_date,
                Timeslot.start_time < appointment_date + timedelta(days=1),
                Timeslot.is_booked == False
                ).all()
    
            return render_template("timeslots.html", timeslots=timeslots)
    else:
        error = "Appointment booking wasn't successfull, please try again."
        return render_template("book_appointment.html", error=error,available_doctors=available_doctors)

# Book timeslot route           
@app.route("/book_timeslot", methods=['POST'])
def book_timeslot():
    available_doctors = Doctor.query.all()
    if request.method == 'POST':
            
                        
            timeslot_id = int(request.form.get('timeslot'))
            username = session['username']
            user = User.query.filter_by(username=username).first()
            timeslot = Timeslot.query.get(timeslot_id)
            timeslot.is_booked = True
            db.session.commit()
            appointment = Appointment(name=name, email=email, message=message, user_id=user.id, doctor_id=doctor_id, timeslot_id= timeslot_id)
            db.session.add(appointment)
            db.session.commit()
            success = 'Appointment booked successfully!'

            return render_template("book_appointment.html", success=success, available_doctors= available_doctors)
        
    else:            
            error = 'There was an issue booking your appointment'
            return render_template("book_appointment.html", error=error, available_doctors= available_doctors)



@app.route("/view")
def view_appointment():
    check_authentication()
    username = session['username']
    user = User.query.filter_by(username=username).first()
    #appointments = Appointment.query.filter_by(user_id=user.id)
    return render_template("view_appointments.html", user = user)

@app.route("/doctor_view")
def doctor_view():
    name = session['username']
    #Doctors view appointments
    doctor = Doctor.query.filter_by(name=name).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return render_template('doctor_view_appointments.html', doctor=doctor, appointments=appointments)



@app.route("/profile")
def view_profile():
    check_authentication()
    username = session['username']
    user = User.query.filter_by(username=username).first()
    return render_template("profile.html", user=user)

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    user_input = request.form['user_input']
    response = asyncio.run(agent.handle_text(user_input))

    '''
    bot_response = response[0]['text']
    message = Message(user_input=user_input, bot_response=bot_response)
    db.session.add(message)
    db.session.commit()
    '''

    return jsonify(response)


@app.route("/chat_page", methods=['POST', 'GET'])
def chat_page():
    """
    messages = Message.query.all()
    """
    return render_template("chat.html")


@app.route('/admin')
def admin_panel():
    return render_template('admin.html', admin=admin)


@app.route('/test')
def test_page():

    doctors = Doctor.query.all()
    timeslots = Timeslot.query.all()

    return render_template('test.html', doctors=doctors, timeslots=timeslots)



