from flask import Flask, session, request, render_template, redirect

app = Flask(__name__)
app.secret_key = "You Will Never Guess"
ponline = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dologin/', methods=['POST'])
def dologin():
    if request.method == 'POST':
        if "useronline" not in session:
            session['useronline'] = 0
        user = request.form['username']
        password = request.form['password']
        if user == "admin" and password == "1234":
            return redirect('/chat.html')
        elif user not in ponline and password == "ozzeano":
            ponline.append(user)
            session['useronline'] += 1
            return "Numero de usuarios online: " + str(session['useronline']) + "<br> Usuarios conectados: <br>" + "".join(x+"<br>" for x in ponline)
        else:
            return redirect('/')

@app.route('/chat.html')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run()