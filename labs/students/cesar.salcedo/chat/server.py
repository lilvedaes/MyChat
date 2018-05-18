from flask import Flask, render_template, session, request, redirect, url_for
from model.entities import *
from database.connector import *

app = Flask(__name__)
app.secret_key = '?'

db = connector.Manager()

engine = db.createEngine()
db_session = db.getSession(engine)



cache = {}

def getUser(id):
    if id not in cache.keys():
        cache[id] = db_session.query(User).filter_by(id = id).first()

    return cache[id]



@app.route('/')
def main():
	return redirect('/login')

@app.route('/login')
def login():
	error = request.args.get('e')

	if error == None:
		return render_template('login.html')

	return render_template('login.html', error = int(error))

@app.route('/register')
def register():
	error = request.args.get('e')

	if error == None:
		return render_template('register.html')

	return render_template('register.html', error = int(error))

@app.route('/register_success')
def register_success():
	return render_template('register_success.html')

@app.route('/chat/<id>')
def chat(id):
	user = db_session.query(User).filter_by(id = id).first()
	count = db_session.query(User).count()

	return render_template('chat.html', user = user, User = User, count = count)



@app.route('/dologin', methods = ['POST'])
def dologin():
    if request.method != 'POST':
        return redirect(url_for('login', e = 1))

    data = request.form

    log_user = User(data['username'], data['password'])
    user = getUser(log_user.id)

    if user == None:
        return redirect(url_for('login', e = 2))

    if user.password != log_user.password:
        return redirect(url_for('login', e = 3))

    return redirect('/chat/' + log_user.id)


@app.route('/doregister/', methods = ['POST'])
def doregister():
    if request.method != 'POST':
        return render_template('register.html', error = 1)

    data = request.form

    user = User(data['username'], data['password'])
    pwc = data['passwordconfirm']

    if user.username == '' or user.password == '' or pwc == '':
        return redirect(url_for('register', e = 2))

    if db_session.query(User).filter_by(id = user.id).first() != None:
        return redirect(url_for('register', e = 3))

    if user.password != pwc:
        return redirect(url_for('register', e = 4))

    db_session.add(user)
    db_session.commit()

    return redirect('/register_success')



db_session.close()

if __name__ == '__main__':
	app.run(debug = True)