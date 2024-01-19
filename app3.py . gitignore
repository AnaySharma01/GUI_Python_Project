#imports packages
from flask import *
import sqlite3
import bcrypt
import time
from adafruit_motorkit import MotorKit
from flask_cors import CORS
import cv2
import numpy as np

#creates new motor kit
kit = MotorKit(0x40)

 #creates flask app
app = Flask(__name__)
CORS(app)

#used for session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Global variable for control
is_running = False

#gets database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#navigates to homepage
@app.route('/')
def index():  
    if 'username' in session:
        return render_template('index.html',firstname=session['username'])
    return render_template('login.html')

#navigates to login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    #checks user credentials
    if request.method == 'POST':
      conn = get_db_connection()
      user = conn.execute('SELECT * from user where username = ? ',
                          (str(request.form['username']),)).fetchone()
      conn.close()
      #checks password
      if bcrypt.checkpw(request.form["password"].encode("utf-8"),str(user["password"]).encode("utf-8")):
          session['username'] = user["first_name"]
          return redirect(url_for('index'))    
      else:
         print("User/ Password Error")

    return render_template('login.html')

#creates registration page
@app.route('/registration',methods=['GET', 'POST'])
def registration():
    #saves user information
    if request.method == 'POST':
        firstname=request.form["fname"]
        lastname=request.form["lname"]
        username=request.form["username"]
        #encrypts password
        salt = bcrypt.gensalt()
        password = (bcrypt.hashpw(request.form["password"].encode("utf-8"),salt).decode(encoding= "utf-8"))
        conn = get_db_connection()
        user = conn.execute('SELECT * from user where username = ? ',
                          (str(request.form['username']),)).fetchone()
        #checks if user is in the database
        if user is None:
             conn.execute('INSERT INTO user (username,password,first_name,last_name) VALUES (?, ?,?,?)',                          
                         (username,password, firstname, lastname ))
        else:
            print(f"User {username} already exist!")
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    else:
     return render_template('registration.html')

#logs out and redirects to login page
@app.route('/logout')
def logout():
    #removes the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

#Routes for controlling the robot
@app.route('/start', methods = ['GET', 'POST'])
def start():
  global is_running
  is_running = True
  # Open webcam
  webcam = cv2.VideoCapture(0)
  while is_running:
      # Read frame from the webcam
      ret, frame = webcam.read()

      # Convert frame to HSV (Hue, Saturation, Value) color space
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Define range for blue color in HSV
      lower_blue = np.array([100, 150, 0])
      upper_blue = np.array([140, 255, 255])

      # Threshold the HSV image to get only blue colors
      mask = cv2.inRange(hsv, lower_blue, upper_blue)

      # Bitwise-AND mask and original image
      blue_edges = cv2.bitwise_and(frame, frame, mask=mask)

      # Convert to grayscale
      gray = cv2.cvtColor(blue_edges, cv2.COLOR_BGR2GRAY)

      # Apply GaussianBlur
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Apply Canny edge detection
      edges = cv2.Canny(blurred, 50, 150)

      # Define a region of interest (ROI)
      roi_vertices = np.array([[(0, frame.shape[0]), (frame.shape[1] // 2, frame.shape[0] // 2),
                                (frame.shape[1], frame.shape[0])]], dtype=np.int32)
      roi_edges = cv2.fillPoly(np.zeros_like(edges), roi_vertices, 255)
      roi = cv2.bitwise_and(edges, roi_edges)

      # Apply Hough transform to detect lines in the ROI
      lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=30)

      # Calculate the center of the lane
      if lines is not None:
          left_line_x = []
          right_line_x = []
          for line in lines:
              x1, y1, x2, y2 = line[0]
              slope = (y2 - y1) / (x2 - x1)
              if slope < 0:  # left line
                  left_line_x.append((x1 + x2) / 2)
              else:  # right line
                  right_line_x.append((x1 + x2) / 2)

          if left_line_x and right_line_x:
              center_x = (np.mean(left_line_x) + np.mean(right_line_x)) / 2
          else:
              center_x = frame.shape[1] / 2

          # Control the motors based on the lane position
          motor_speed = (center_x - frame.shape[1] // 2) / (frame.shape[1] // 2)

          # Forward and backward motion
          kit.motor1.throttle = 0.5 + motor_speed
          kit.motor2.throttle = 0.5 - motor_speed

          # Check for stop signal
          if not is_running:
              break
      else:
          # If no lines are detected, stop the motors
          kit.motor1.throttle = 0
          kit.motor2.throttle = 0

      # Display the frame
      cv2.imshow("Frame", frame)

      # Break the loop when 'q' is pressed
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  # Release the webcam and close all windows
  webcam.release()
  cv2.destroyAllWindows()
  #starts robot and let the robot to move following a lane with webcam
  return jsonify("start")

 #Move the robor right    
@app.route('/right', methods = ['GET', 'POST'])
def right():
  #moves robot right
  kit.motor1.throttle = -0.72
  kit.motor2.throttle = 0.72
  #runs both motors for 0.3 seconds
  time.sleep(0.3)
  return jsonify("right")

 #Move the robot forward
@app.route('/forward', methods = ['GET', 'POST'])
def forward():
  #moves robot forward
  kit.motor1.throttle = 0.732
  kit.motor2.throttle = 0.7
  #runs both motors for 0.3 seconds
  time.sleep(0.3)
  return jsonify("forward")
@app.route('/backward', methods = ['GET', 'POST'])
#Move the robot backward
def backward():
  #moves robot backwards
  kit.motor1.throttle = -0.81
  kit.motor2.throttle = -0.7
  #runs both motors for 0.3 seconds
  time.sleep(0.3)
  return jsonify("backward")

@app.route('/left', methods = ['GET', 'POST'])
#Move the robot left
def left():
  #moves robot left
  kit.motor1.throttle = 0.72
  kit.motor2.throttle = -0.75
  #runs both motors for 0.3 seconds
  time.sleep(0.3)
  return jsonify("left")
#Stop the robot
@app.route('/stop', methods = ['GET', 'POST'])
def stop():
  global is_running
  is_running = False
  #stops both motors
  kit.motor1.throttle = 0
  kit.motor2.throttle = 0
  return jsonify("stop")

#Allows app to run
if __name__ == '__main__':
    app.run(host='192.168.1.17', port=4444)
