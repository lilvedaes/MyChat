from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = "You Will Never Guess"

@app.route("/")
def login_page():
    return render_template('HTML.html')

@app.route('/dologin/', methods=['POST'])
def dologin():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['passw']

        if "useronline" not in session:
            session['useronline'] = 0

        if user == "admin" and passw == "1234":
            return redirect('/ChatPage.html')
        elif passw == "1234":
            session['useronline'] += 1
            return "Active online users: " + str(session['useronline'])
        else:
            return redirect ('/')

@app.route("/ChatPage.html")
def chat_page():
    return render_template('ChatPage.html')

if __name__ == '__main__':
    app.run()
