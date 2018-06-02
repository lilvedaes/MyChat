from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
    return render_template('loginSDLG.html')

@app.route("/chatSDLG.html")
def chat_page():
    return render_template('chatSDLG.html')

if __name__ == "__main__":
    app.run()