from flask import Flask, render_template, session, request


app = Flask(__name__)
app.secret_key = 'you will never guess'


@app.route("/")
def main():
    return render_template('login.html')




@app.route('/login', methods = ['POST'])
def login():
    global usuario
    if request.method == 'POST':
        data = request.form
        if(data['username']=="jorge" and data['password']=="mayna"):
            session[data['username']] = data['username']
            usuario = data['username']
            return render_template('chaat.html', nombre=usuario)
        elif(data['username']=="dylan" and data['password']=="castro"):
            session[data['username']] = data['username']
            usuario = data['username']
            return render_template('chaat.html',nombre=usuario)
        elif (data['username'] == "elena" and data['password'] == "benel"):
            session[data['username']] = data['username']
            usuario = data['username']
            return render_template('chaat.html',nombre=usuario)
        elif (data['username'] == "el pro" and data['password'] == "io"):
            session[data['username']] = data['username']
            usuario = data['username']
            return render_template('chaat.html',nombre=usuario)
        else:
            return render_template('login.html')



@app.route('/logout')
def logout():

    session.pop(usuario, None)
    return render_template('login.html')


if __name__ == "__main__":
    app.run()