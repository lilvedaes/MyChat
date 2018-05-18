from flask import  Flask, session, request, render_template

app=Flask(__name__)

@app.route('/')
def main():
    return render_template("login.html")

@app.route('/chat')
def chat():
    return render_template("chat.html")

if __name__=='__main__':
    app.run()