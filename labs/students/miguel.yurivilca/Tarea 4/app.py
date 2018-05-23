from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

cache={}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dologin', methods=['POST'])
def dologin():
    if request.method == 'POST':
        if request.form['username'] == 'username' and request.form['password'] == 'password':
            return redirect(url_for('chat'))
        else:
            return redirect(url_for('login'))


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/registration')
def registration():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    from database import init_db
    init_db()
    from database import Session
    session = Session()
    from models import User
    if request.method == 'POST':
        if request.form['password'] == request.form['vpassword']:
            user = User(request.form['username'], request.form['password'])
            session.add(user)
            session.commit()
            session.close()
        else:
            return render_template('login.html')
    return render_template('registrationSuccessful.html')


@app.route('/getUsers', methods=['GET'])
def getUsers():
    key = 'getUsers'
    from database import init_db
    init_db()
    from database import Session, engine
    from models import User, AlchemyEncoder

    if key not in cache.keys():
        session = Session()
        DbResponse = session.query(User)
        cache[key]=DbResponse
        print("From DB")
    else:
        print("From Cache")
    users = cache[key]
    response =[]
    for user in users:
        response.append(user)
    return json.dumps(response, cls=AlchemyEncoder)


if __name__ == '__main__':
    app.run()