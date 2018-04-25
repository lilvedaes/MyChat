from flask import Flask, render_template
#!/usr/local/bin/python

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run()
