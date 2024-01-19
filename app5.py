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
import GUI 
import detection

#Runs motor functions
runGUI()

#Detects the lines
detectLines()

# Global variable for control
is_running = False

#Generates raw video
def generate_raw_video():
  global webcam
  webcam = cv2.VideoCapture(0)
  webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 256)  # Set width
  webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)  # Set height
  while True:
      success, frame = webcam.read()
      if not success:
          break
      else:
          ret, buffer = cv2.imencode('.jpg', frame)
          frame = buffer.tobytes()
          yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Generates image processed video
def generate_processed_video():
    global webcam
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 256)  # Set width
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)  # Set height
    while True:
        success, frame = webcam.read()
        if not success:
            break
        else:
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

#Route for starting the video feed
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

    #Threshold the HSV image to get only blue colors
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


#Stops the robot
@app.route('/stop', methods = ['GET', 'POST'])
def stop():
  global is_running,webcam
  is_running = False
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

