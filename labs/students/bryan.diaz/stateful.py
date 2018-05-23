from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

@app.route('/setuser/<username>')
def setuser(username):
    if 'username' not in session:
        session['username'] = ''
    session['username'] = str(session['username']) + " " + str(username)
    return 'Username registered: ' + username

@app.route('/numbuser')
def quantity():
    num=0
    for num in range(0, len(session['username'].split())):
        num+=1
    return "The number of registered users is: " + str(num)

@app.route('/online_users')
def online():
    return "Online Users: " + " "+ session['username']

if __name__ =='__main__':
    app.run()