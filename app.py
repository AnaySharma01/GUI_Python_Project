#imports packages
from flask import *
import sqlite3 
import bcrypt
import time
# from adafruit_motorkit import Motorkit

 #creates flask app
app = Flask(__name__)
#used for session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

@app.route('/login',methods=['GET', 'POST'])
def login( ):
    #gets user
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
def registration( ):
    #saves user
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
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/right')
def right():
    if 'username' in session:
        # # Right turn
        # kit.motor1.throttle = -0.72
        # kit.Motor2.throttle = 0.72
        # time.sleep(0.79)

        return jsonify("right")
    else:
       return jsonify("not logged in")
@app.route('/forward')
def forward():
    if 'username' in session:
        # # Forward at full speed
        # kit.motor1.throttle = 0.732
        # kit.motor2.throttle = 0.7
        # #Run both motors for 3.5 seconds
        # time.sleep(3.5)

        return jsonify("forward")
    else:
       return jsonify("not logged in")
@app.route('/backward')
def backward():
    if 'username' in session:
        # #Backward at full speed
        # kit.motor1.throttle = -0.81
        # kit.motor2.throttle = -0.7
        # # Run both motors for 3.5 seconds
        # time.sleep(3.5)
        return jsonify("backward")
    else:
       return jsonify("not logged in")
@app.route('/left')
def left():
    if 'username' in session:
    #     #Left turn
    #     kit.motor1.throttle = -0.72
    #     kit.Motor2.throttle = 0.75
    #     time.sleep(1.5)

        return jsonify("left")
    else:
       return jsonify("not logged in")

#Allows app to run
if __name__ == '__main__':
    app.run(host='192.168.1.28', port=4444)
    #kit = Motorkit(0x40)
