from flask import Flask, flash, render_template, session, request, redirect, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if 'count' not in session:
        session['count'] = 0
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('chats.html')

@app.route('/Users/<string:user>')
def newUser(user):
    if 'count' not in session:
        session['count'] = 0
    if user not in session:
        session[user] = ''
        session['count'] += 1
    return users()

def users():
    str1 =  "Hay " + str(session['count']) + " usuario(s) conectado(s): \n"
    for i in session:
        if i != 'logged_in' and i != 'count':
            str1 += i + "\n"
    return str1

@app.route('/login', methods = ['POST'])
def login():
    if 'count' not in session:
        session['count'] = 0
    if request.form["password"] == 'Rojas' and request.form["username"] == 'Reynaldo':
        session['logged_in'] = True
    else:
        flash('Wrong password')
    return home()

@app.route('/logout')
def logout():
    if 'count' not in session:
        session['count'] = 0
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
