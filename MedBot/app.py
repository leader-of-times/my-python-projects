from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import os, sys

app = Flask(__name__)

app.secret_key = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
app.config['SQLALCHEMY_BINDS'] = {
    'doctors': 'sqlite:///doctors.db',
    'patients': 'sqlite:///patients.db'
}

db = SQLAlchemy(app)

class Doctor(db.Model):
    __bind_key__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Patient(db.Model):
    __bind_key__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']

        if user_type == 'doctor':
            if Doctor.query.filter_by(email=email).first():
                return "Doctor already exists!", 400
            new_user = Doctor(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        elif user_type == 'patient':
            if Patient.query.filter_by(email=email).first():
                return "Patient already exists!", 400
            new_user = Patient(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        else:
            return "Invalid user type!", 400

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        if not email or not password or not user_type:
            return render_template('login.html', error="Please fill in all fields.")

        user = Doctor.query.filter_by(email=email).first() if user_type == 'doctor' else Patient.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user_type
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_type=session['user_type'])

@app.route('/start_chatbot')
def start_chatbot():
    try:
        streamlit_script_path = os.path.join(os.getcwd(), 'chatbot/chatbot.py')

        process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", streamlit_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            return redirect("http://localhost:8501")
        else:
            return f"Error starting Streamlit: {stderr.decode()}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
