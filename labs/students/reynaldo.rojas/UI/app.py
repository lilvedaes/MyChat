from flask import Flask, flash, render_template, session, request, redirect, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('chats.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.form["password"] == 'Rojas' and request.form["username"] == 'Reynaldo':
        session['logged_in'] = True
    else:
        flash('Wrong password')
    return home()
    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
