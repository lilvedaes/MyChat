
from flask import Flask, render_template, redirect, url_for, request, session



app=Flask(__name__)

datos={
        'jbellido' : 'jbellido'

}


@app.route('/')
def index():
    return render_template('login.html')



@app.route('/',methods=['POST'])
def before():
    if request.method == 'POST':
        session['username'] = request.form['uname']
        session['password'] = request.form['pwd']
        global datos
        if session['username'] in datos and session['password'] == datos[session['username']]:
            return redirect(url_for('chat'))
        else:
            return render_template('login.html')

@app.route('/chat')
def chat():
	return render_template('chat.html')

if __name__=='__main__':
    app.secret_key = 'clavecita'
    app.run(debug=True)
