from flask import render_template, request, session, redirect, url_for, jsonify
from index import app, admin, db
from index.models import User, Appointment, Message
import asyncio
import rasa
from rasa.core.agent import Agent

model_path = "index/models/20230419-014324-numerous-vertex.tar.gz"
agent = Agent.load(model_path)


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
            success = "Logged in successfully"
            return render_template("home.html", success=success)
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
    return render_template("home.html")

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
            
            return render_template("take_test.html", score = score)
    
    else:

        return render_template('take_test.html')



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

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    user_input = request.form['user_input']
    response = asyncio.run(agent.handle_text(user_input))


    bot_response = response[0]['text']
    message = Message(user_input=user_input, bot_response=bot_response)
    db.session.add(message)
    db.session.commit()


    return jsonify(response)


@app.route("/chat_page", methods=['POST', 'GET'])
def chat_page():

    messages = Message.query.all()
    return render_template("chat.html", messages=messages)


@app.route('/admin')
def admin_panel():
    return render_template('admin.html', admin=admin)


@app.route('/test')
def test_page():

    messages = Message.query.all()

    return render_template('test.html', messages=messages)



