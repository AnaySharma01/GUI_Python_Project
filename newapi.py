from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time

kit = MotorKit(0x40)
app = Flask(__name__)

@app.route('/')


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

def forward(amount_of_time_to_run):
    kit.motor1.throttle = -0.6
    kit.motor2.throttle = 0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def backward(amount_of_time_to_run):
    kit.motor1.throttle = 0.7
    kit.motor2.throttle = -0.7
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def left(amount_of_time_to_run):
    kit.motor1.throttle = -0.64
    kit.motor2.throttle = -0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def right(amount_of_time_to_run):
    kit.motor1.throttle = 0.64
    kit.motor2.throttle = 0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def stop():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

if __name__ == '__main__':
    app.run(host='192.168.1.15', port=5000)
