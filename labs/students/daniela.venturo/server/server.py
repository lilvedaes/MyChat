from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')
@app.route("/")
def main():
    return render_template('login.html')

@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()