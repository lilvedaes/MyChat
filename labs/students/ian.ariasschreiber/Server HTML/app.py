from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
    return render_template('myChat.html')

@app.route('/ActualChat.html')
def ActualChat():
    return render_template('ActualChat.html')


if __name__ == '__main__':
    app.run(debug=True)
