#imports packages
from flask import Flask,session,jsonify
from flask import request,render_template,redirect,url_for
import sqlite3 
import bcrypt
from GUI import app,get_db_connection

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
