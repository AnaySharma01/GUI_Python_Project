#imports packages
from flask import Flask,session,jsonify
from flask import request,render_template,redirect,url_for
import sqlite3 
import bcrypt
from GUI import app,get_db_connection

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
