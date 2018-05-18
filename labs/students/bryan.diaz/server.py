from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login2.html')

@app.route("/dologin/", methods = ['POST'])
def dologin():
    if request.method == 'POST':
        data = request.form #a multidict containing POST data
        if data['username'] == 'alumno' and data['password'] == 'csutec1234':
            return render_template('chat.html')
        else:
            return render_template('login2.html')

@app.route("/dologin/setUsers")
def setUsers():
    return 'username'

if __name__ == "__main__":
    app.run()