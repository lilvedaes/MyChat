from flask import Flask, session

app = Flask(__name__)
app.secret_key= 'You Will Never Guess'

@app.route('/userset/<user>')
def set(user):
    if 'usuarios' not in session:
        session['usuarios']= ''
    session['usuarios']= str(session['usuarios'])+' '+str(user)

    return "Tu usuario esta registrado: " + user

@app.route('/viewusers')
def view():
    return session['usuarios']

@app.route('/count')
def count():
    x=len(session['usuarios'].split(' '))-1
    return str(x)


if __name__ == '__main__':
    app.run()
