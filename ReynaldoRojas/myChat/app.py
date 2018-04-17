from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def loginF():
    return render_template('login.html')

@app.route('/chats')
def chatsF():
    return render_template('chats.html')

if __name__ == "__main__":
    app.run(debug=True)
