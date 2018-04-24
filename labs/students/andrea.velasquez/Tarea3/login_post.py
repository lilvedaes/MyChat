import time
from flask import Flask, session, request, render_template, redirect

app = Flask(__name__)
app.secret_key = "You Will Never Guess"
allusers = []


@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/dologin', methods=['POST', 'GET'])
def dologin():
    if request.method == 'POST':

        user = request.form['user']
        passw = request.form['pass']

        if user == "admin" and passw == "123":
            return render_template('Chat.html')
        elif user not in allusers and passw == "other":
            allusers.append(user)
            return "<h1>Active Users</h1>" + "<p>The number of active users is: " + str(len(allusers)) + "</p>" + "<h4>List of users:</h4>" + "".join("<p>"+x+"</p>" for x in allusers)
        else:
            time.sleep(1)
            return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
