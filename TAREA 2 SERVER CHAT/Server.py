from flask import Flask, render_template, session, request

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/dologin', methods = ['POST'])
def dologin():
    if request.method == 'POST':
        data = request.form
        if data['uname'] == "jbellido" and data['pname'] == "12345678":
            return render_template('Chat.html')
        else:
            return render_template('Login.html')
"""""
@app.route('/Chat.html')
def chat():
    return render_template('Chat.html')
"""""
if __name__ == '__main__':
    app.run()
