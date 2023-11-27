#imports packages
from flask import *
from flask import Flask,session,jsonify
from flask import request,render_template,redirect,url_for
import sqlite3 
import bcrypt
import time
from adafruit_motorkit import MotorKit

#creates new motor kit
kit = MotorKit(0x40)

 #creates flask app
app = Flask(__name__)

#used for session 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#gets database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Routes for controlling the robot
@app.route('/started')
def start():
    #starts robot
    if 'username' in session:
          return jsonify("started")
    else:
       return jsonify("not logged in")
 #Move the robot right
@app.route('/right')
def right():
    if 'username' in session:
          #moves robot right
          kit.motor1.throttle = -0.72
          kit.motor2.throttle = 0.72
          #runs both motors for 0.3 seconds
          time.sleep(0.3)

          return jsonify("right")
    else:
       return jsonify("not logged in")
 #Move the robot forward
@app.route('/forward')
def forward():
    if 'username' in session:
          #moves robot forward 
          kit.motor1.throttle = 0.732
          kit.motor2.throttle = 0.7
         #runs both motors for 0.3 seconds
          time.sleep(0.3)
          return jsonify("forward")
    else:
       return jsonify("not logged in")
@app.route('/backward')
#Move the robot backward
def backward():
    if 'username' in session:
          #moves robot backwards
          kit.motor1.throttle = -0.81
          kit.motor2.throttle = -0.7
          #runs both motors for 0.3 seconds
          time.sleep(0.3)
          return jsonify("backward")
    else:
       return jsonify("not logged in")
@app.route('/left')
#Move the robot left
def left():
    if 'username' in session:
         #moves robot left
         kit.motor1.throttle = 0.72
         kit.motor2.throttle = -0.75
         #runs both motors for 0.3 seconds
         time.sleep(0.3)

         return jsonify("left")
    else:
       return jsonify("not logged in")

@app.route('/move')
#Moves the robot
def moveRobot():

    rbt_direction = request.args.get('direction')
    rbt_turn = float(request.args.get('turn'))
    rbt_time = float(request.args.get('time'))
    if rbt_direction == 'forward':
        #moves robot forward
          kit.motor1.throttle = 0.732
          kit.motor2.throttle = 0.7
         #runs both motors for _ seconds
          time.sleep(rbt_time)
          #stops both motors
          kit.motor1.throttle = 0
          kit.motor2.throttle = 0
    elif rbt_direction == 'backward':
        # moves robot backwards
        kit.motor1.throttle = -0.81
        kit.motor2.throttle = -0.7
        # runs both motors for _ seconds
        time.sleep(rbt_time)
        # stops both motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    elif rbt_direction == 'left':
        # moves robot backwards
        # moves robot left
        kit.motor1.throttle = 0.72
        kit.motor2.throttle = -0.75
        # runs both motors for _ seconds
        time.sleep(rbt_turn*(0.6/90))
        # stops both motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    elif rbt_direction == 'right':
        # moves robot right
        kit.motor1.throttle = -0.72
        kit.motor2.throttle = 0.72
        # runs both motors for _ seconds
        time.sleep(rbt_turn*(0.6/90))
        # stops both motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    elif rbt_direction == 'stop':
        # stops robot
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    
    return jsonify("success")

#Stops the robot
@app.route('/stop')
def stop():
    if 'username' in session:
          #stops both motors
          kit.motor1.throttle = 0
          kit.motor2.throttle = 0

          return jsonify("stop")
    else:
       return jsonify("not logged in")
