from flask import Flask, render_template, send_from_directory
app = Flask(__name__, static_url_path='')



@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/chat')
def hello1():
    return render_template("chatbox2.html")

# localhost:5000/static/avatar.png
@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory("statics", path)

if __name__ == "__main__":
    app.run()
