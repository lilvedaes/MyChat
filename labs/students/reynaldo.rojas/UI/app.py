from flask import Flask, flash, render_template, session, request, redirect, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tableini import *

engine = create_engine('sqlite:///data.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home():
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

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]),User.password.in_([POST_PASSWORD]))
    result = query.first()

    if result:
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
