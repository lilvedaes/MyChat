from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def login_page():
    return render_template('HTML.html')

@app.route("/ChatPage.html")
def chat_page():
    return render_template('ChatPage.html')

if __name__ == "__main__":
    app.run()
