from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def login_page():
    return render_template('Login.html')


@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
