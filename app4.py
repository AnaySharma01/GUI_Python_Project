#imports packages
from flask import *
import sqlite3
import bcrypt
import time
from adafruit_motorkit import MotorKit
from flask_cors import CORS
import cv2
import numpy as np
from flask import Response

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

# Masking
def mask_img(img):  # H  S  V
    lower_thr = np.array([0, 0, 0])
    upper_thr = np.array([179, 255, 87])
    img_masked = cv2.inRange(img, lower_thr, upper_thr)
    return img_masked

# Canny Edge Detection
def detect_edges(img):
  img_gre = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(img_gre, (5, 5), 0)
  img_canny = cv2.Canny(blur, 200, 400)
  return img_canny

# Cropping , Region of Interest
def crop_roi(img):
    height = img.shape[0]
    width = img.shape[1]
    # print(height, width)
    mask = np.zeros_like(img)
    cv2.rectangle(mask, (0, height // 2), (width, height), 255, -1)  # -1 -> fill
    roi = cv2.bitwise_and(img, mask)
    return roi

# Hough Transform
def detect_lines(img):
    # function that we use is HoughLinesP
    rho = 1
    theta = np.pi / 180
    min_threshold = 10
    min_line_length = 20
    max_line_gap = 4
    lines = cv2.HoughLinesP(img, rho, theta, min_threshold, np.array([]), min_line_length, max_line_gap)
    return lines
  
# Group positive slope and negative slope lines, which will define left and right lane markings
def group_lines(img, lines):
    height = img.shape[0]
    width = img.shape[1]
    lane_lines = []
    # No lines found
    if lines is None:
        return lane_lines
    left_lane = []
    right_lane = []
    boundary = 1 / 3
    left_lane_area_width = width * (1 - boundary)
    right_lane_area_width = width * boundary
    for line in lines:
        for x1, y1, x2, y2 in line:
            # skip vertical lines as they have infinite slope
            if x1 == x2:
                continue
            coff = np.polyfit((x1, x2), (y1, y2), 1)
            slope = coff[0]
            intercept = coff[1]
            # positive slop -> right lane marking  \
            #                                       \
            #                                        \
            #                                         \
            if slope > 0:
                # search area check
                if x1 > right_lane_area_width and x2 > right_lane_area_width:
                    right_lane.append((slope, intercept))
            # negative slop -> left lane marking  /
            #                                    /
            #                                   /
            #                                  /
            else:
                if x1 < left_lane_area_width and x2 < left_lane_area_width:
                    left_lane.append((slope, intercept))

    # averaging all the lines in each group to get a single line out of them
    left_avg = np.average(left_lane, axis=0)
    right_avg = np.average(right_lane, axis=0)

    # if got left lane, convert to point form from intercept form
    if len(left_lane) > 0:
        lane_lines.append(line_to_point(img, left_avg))
    if len(right_lane) > 0:
        lane_lines.append((line_to_point(img, right_avg)))
    return lane_lines

# Create points from the lane lines with slop and intercept
def line_to_point(img, line):
    slop = line[0]
    intercept = line[1]
    height = img.shape[0]
    width = img.shape[1]
    y1 = int(height / 2)  # middle
    x1 = int((y1 - intercept) / slop)
    if x1 < 0:
        x1 = 0
    if x1 > width:
        x1 = width
    y2 = int(height)  # bottom
    x2 = int((y2 - intercept) / slop)
    if x2 < 0:
        x2 = 0
    if x2 > width:
        x2 = width
    return [[x1, y1, x2, y2]]

def generate_raw_video():
  global webcam
  webcam = cv2.VideoCapture(0)
  webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 256)  # Set width
  webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)  # Set height

  # Set the desired frame rate
  frame_rate = 5  # You can adjust this value
  prev_frame_time = 0

  while True:
      time_elapsed = time.time() - prev_frame_time
      success, frame = webcam.read()
      # if not success:
      #     break
      # if time_elapsed > 1./frame_rate:
      #     prev_frame_time = time.time()
      #     # Apply JPEG compression
      #     ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])  
      #     frame = buffer.tobytes()
      #     yield (b'--frame\r\n'
      #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def generate_processed_video():
    global webcam
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 256)  # Set width
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)  # Set height
    # Set the desired frame rate
    frame_rate = 20  # Adjust as needed
    prev_frame_time = 0

    while True:
        time_elapsed = time.time() - prev_frame_time
        success, frame = webcam.read()
        if not success:
            break

        if time_elapsed > 1./frame_rate:
            prev_frame_time = time.time()

            # Existing processing code...
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = mask_img(hsv)
            edges = detect_edges(mask)
            cropped = crop_roi(edges)
            lines = detect_lines(cropped)
            lane_lines = group_lines(frame, lines)

            if lane_lines:
                for line in lane_lines:
                    cv2.line(frame, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 2)

            if len(lane_lines) == 2:
                mid_x1 = (lane_lines[0][0][0] + lane_lines[1][0][0]) // 2
                mid_y1 = (lane_lines[0][0][1] + lane_lines[1][0][1]) // 2
                mid_x2 = (lane_lines[0][0][2] + lane_lines[1][0][2]) // 2
                mid_y2 = (lane_lines[0][0][3] + lane_lines[1][0][3]) // 2
                cv2.line(frame, (mid_x1, mid_y1), (mid_x2, mid_y2), (0, 255, 0), 2)

            # Apply JPEG compression
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85]) 
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
  global is_running, kit, webcam
  is_running = True
  while is_running:
    # Read frame from the webcam
    ret, frame = webcam.read()
    if not ret:
      break
    frame = cv2.resize(frame, (640, 480))    
    # Convert frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = mask_img(hsv)
    # Bitwise-AND mask and original image
    edges = detect_edges(mask)
    cropped = crop_roi(edges)
    lines = detect_lines(cropped)
    lines_grouped = group_lines(frame, lines)
    if(len(lines_grouped) == 1):
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
  global is_running,webcam
  is_running = False
  #stops both motors
  kit.motor1.throttle = 0
  kit.motor2.throttle = 0
  # Release the webcam 
  webcam.release()
  return jsonify("stop")

@app.route('/video_feed_raw', methods = ['GET', 'POST'])
def video_feed_raw():
    return Response(generate_raw_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_processed',methods = ['GET', 'POST'])
def video_feed_processed():
    return Response(generate_processed_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#Allows app to run
if __name__ == '__main__':
    app.run(host='192.168.1.28', port=3333)
