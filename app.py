#imports packages
from flask import *
from flask import Flask,session,jsonify
from flask import request,render_template,redirect,url_for

#imports app modules
from GUI import app
import registration
import login
import GUI

#navigates to homepage
@app.route('/')
def index():   
    if 'username' in session:
        return render_template('index.html',firstname=session['username'])
    return render_template('login.html')

#logs out and redirects to login page
@app.route('/logout')
def logout():
    #removes the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

#Allows app to run
if __name__ == '__main__':
    app.run(host='192.168.1.28', port=4444)
