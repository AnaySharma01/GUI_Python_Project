from flask import Flask, request, jsonify

from adafruit_motorkit import MotorKit

import time



app = Flask(__name__)





@app.route('/')

def index():

    return '''

            <!DOCTYPE html>

        <html lang="en" dir="ltr">

          <head>

            <meta charset="utf-8">

            <title>Control Panel</title>

          </head>

          <style>

            h1

        {text-align: center;}

        h2

        {text-align: center;}

        h3

        {text-align: center;}

        button

        {text-align: center;}

        p

        {text-align: center; font-size: large;}

        body

          {background-color:white;

              color: black;}

        .dark-mode {

          background-color: black;

          color: white;

        }



          .tab {

            overflow: hidden;

            border: 1px solid #ccc;

            background-color: #f1f1f1;

          }

          .tab button {

            background-color: inherit;

            float: left;

            border: none;

            outline: none;

            cursor: pointer;

            padding: 14px 16px;

            transition: 0.3s;

          }

          .tab button:hover {

            background-color: #ddd;

          }

          .tab button.active {

            background-color: #ccc;

          }

          .tabcontent {

            display: none;

            padding: 6px 12px;

            border: 1px solid #ccc;

            border-top: none;

          }

        .cool{float: right;}

        .col{float: left;}

        table, th, td {

  border: 1px solid white;

  border-collapse: collapse;

}

        figcaption{text-align: center;}

        h4{text-align: center;}

        figure {

          border: 1px #cccccc solid;

          padding: 4px;

          margin: auto;

        }



        figcaption {

          background-color: black;

          color: white;

          font-style: italic;

          padding: 2px;

          text-align: center;

        }

        .nice {

          text-align: center;

          list-style-position: inside;

        }

        .po{font-size: small; color: red;}

        </style>

        <script>

        function send_command(direction) {

            fetch('/move', {

                method: 'POST',

                headers: {

                    'Content-Type': 'application/json'

                },

                body: JSON.stringify({ 'direction': direction })

            })

            .then(response => response.json())

            .then(data => console.log(data))

            .catch(error => console.error('Error:', error));

                }

        </script>





          <body id="jeff">

<table style = "width:100%;border: 1px solid black;">

  <tr style = "height:700px;border: 1px solid black;">

    <th style = "width:50%;border: 1px solid black;">something</th>

    <th style="border: 1px solid black;"><table style = "width:100%;">

  <tr style = "height:233px">

    <th style = "width:33%"></th>

    <th style = "width:33%"><button style="height:218px;width:90%;font-size: 50px;" onclick="send_command('forward')" >/\</button></th>

    <th></th>

  </tr>

  <tr style = "height:233px">

    <td><p><button style="height:217px;width:90%;font-size: 55px;" onclick="send_command('left')"><</button></p></td>

    <td><p><button style="height:217px;width:90%;font-size: 50px;background-color: red;" onclick="send_command('stop')">stop</button></p></td>

    <td><p><button style="height:217px;width:90%;font-size: 55px;" onclick="send_command('right')">></button></p></td>



  </tr>

  <tr style = "height:233px">

    <td></td>

    <td><p><button style="height:218px;width:90%;font-size: 50px;" onclick="send_command('backward')">\/</button></p></td>

    <td><p></p></td></table></th>

  </tr>

  <tr style = "height:700px;border: 1px solid black;">

    <td style="border: 1px solid black;"><p>line</p></td>

    <td style="border: 1px solid black;"><p>log</p></td>

  </tr>



</table>

  </body>

        </html>

                        '''



# Create a dictionary to store the robot's current state eg. stopped

robot_state = "stopped"



# Initialize the MotorKit

kit = MotorKit(0x40)



# Define movement functions

def move_forward():

    kit.motor1.throttle = 0.77

    kit.motor2.throttle = 0.73


    robot_state = "moving forward"

def move_backward():

    kit.motor1.throttle = -0.80

    kit.motor2.throttle = -0.76

    robot_state = "moving backward"



def turn_left():

    kit.motor1.throttle = 0.75

    kit.motor2.throttle = -0.75

    robot_state = "turning left"



def turn_right():

    kit.motor1.throttle = -0.76

    kit.motor2.throttle = 0.75

    robot_state = "turning right"



def stop_robot():

    kit.motor1.throttle = 0.0

    kit.motor2.throttle = 0.0

    robot_state = "stopped"

#endpoint to receive movement commands

@app.route('/move', methods=['POST'])

def move_robot():

    global robot_state

    data = request.get_json()

    direction = data.get('direction') #direction sent from send_command()

    # move robot based on the 'direction' received

    if direction == 'forward':

        move_forward()

    elif direction == 'backward':

        move_backward()

    elif direction == 'left':

        turn_left()

    elif direction == 'right':

        turn_right()

    elif direction == 'stop':

        stop_robot()



    return jsonify({'message': f"Robot is now {robot_state}"}) #prints what state the robot is currently in.



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000) #must be using 0.0.0.0 because this ensures that the server can be accessed from other computers.

#the default 127.0.0.1 doesnt allow other computers except the one running the server to process requests.

