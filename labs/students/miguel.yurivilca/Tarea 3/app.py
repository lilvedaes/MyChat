from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)