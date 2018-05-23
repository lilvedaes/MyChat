from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
app = Flask(__name__)
app.secret_key= "abc"

def uy():
    users = 'cantidad de usuarios ' + str(session['counter'])
    for i in session:
        if i!= 'counter' and i!='logged_in':
            users+= ' ' + i
    return users

@app.route('/user/<string:username>')
def show_user_profile(username):
    if 'counter'not in session:
        session['counter']=0
    if username not in session:
        session[username] = 'chalala'
        session['counter']+=1
    return uy()

 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('cuadro.html')
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'Interbank' and request.form['username'] == 'Mariella':
        session['logged_in'] = True
        return home()
    else:
        success_message= 'Ha ingresado el usuario o la contraseña incorrecta. Inténtelo otra vez.'
        flash(success_message) 
        return render_template('login.html')
       
        
    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
