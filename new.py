# Import necessary packages
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import bcrypt
import time
from adafruit_motorkit import MotorKit

# Create a Flask app
app = Flask(__name)
# Set a secret key for sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Navigate to the homepage
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', firstname=session['username'])
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        user = conn.execute('SELECT * from user where username = ?',
                            (str(request.form['username']),)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(request.form["password"].encode("utf-8"), str(user["password"]).encode("utf-8")):
            session['username'] = user["first_name"]
            return redirect(url_for('index'))
        else:
            print("User/Password Error")

    return render_template('login.html')

# Registration route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        firstname = request.form["fname"]
        lastname = request.form["lname"]
        username = request.form["username"]
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), salt).decode(encoding="utf-8")

        conn = get_db_connection()
        user = conn.execute('SELECT * from user where username = ?',
                            (str(request.form['username']),)).fetchone()

        if user is None:
            conn.execute('INSERT INTO user (username, password, first_name, last_name) VALUES (?, ?, ?, ?)',
                         (username, password, firstname, lastname))
        else:
            print(f"User {username} already exists!")
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    else:
        return render_template('registration.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Motor control routes
@app.route('/right')
def right():
    if 'username' in session:
        kit = MotorKit()
        kit.motor1.throttle = -0.72
        kit.motor2.throttle = 0.72
        time.sleep(0.79)
        return jsonify("right")
    else:
        return jsonify("not logged in")

@app.route('/forward')
def forward():
    if 'username' in session:
        kit = MotorKit()
        kit.motor1.throttle = 0.732
        kit.motor2.throttle = 0.7
        time.sleep(3.5)
        return jsonify("forward")
    else:
        return jsonify("not logged in")

@app.route('/backward')
def backward():
    if 'username' in session:
        kit = MotorKit()
        kit.motor1.throttle = -0.81
        kit.motor2.throttle = -0.7
        time.sleep(3.5)
        return jsonify("backward")
    else:
        return jsonify("not logged in")

@app.route('/left')
def left():
    if 'username' in session:
        kit = MotorKit()
        kit.motor1.throttle = -0.72
        kit.motor2.throttle = 0.75
        time.sleep(1.5)
        return jsonify("left")
    else:
        return jsonify("not logged in")

# Run the Flask app
if __name__ == '__main__':
    app.run(host='192.168.1.15', port=4444)

from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time

kit = MotorKit(0x40)
app = Flask(__name__)

# Define the routes for both root and '/control'
@app.route('/')
def home():
    return "Hello, this is a robot control server!"

@app.route('/control', methods=['POST'])
def control():
    command = request.json['command']
    if command == 'forward':
        forward(2.6)
    elif command == 'backward':
        backward(2.6)
    elif command == 'left':
        left(2.6)
    elif command == 'right':
        right(2.6)
    elif command == 'stop':
        stop()
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'})

    return jsonify({'status': 'success', 'message': 'Command executed'})

# Move forward function
def forward(amount_of_time_to_run):
    kit.motor1.throttle = 0.6
    kit.motor2.throttle = -0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

# Move backward function
def backward(amount_of_time_to_run):
    kit.motor1.throttle = -0.7
    kit.motor2.throttle = 0.7
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

# Turn left function
def left(amount_of_time_to_run):
    kit.motor1.throttle = -0.64
    kit.motor2.throttle = -0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

# Turn right function
def right(amount_of_time_to_run):
    kit.motor1.throttle = 0.64
    kit.motor2.throttle = 0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

# Stop function
def stop():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4445)  # Changed host to allow external access

