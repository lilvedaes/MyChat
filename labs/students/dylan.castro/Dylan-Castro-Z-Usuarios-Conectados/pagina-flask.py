from flask import Flask, render_template, request, session,escape
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('login.html')
@app.route('/login', methods = ['POST'])
def login():
    global usuario
    if request.method == 'POST':
        data = request.form
        print(data['username'])
        print(data['password'])
        usuario=data['username']
        if(data['username']=="dylan" and data['password']=="castro"):
            session[usuario] = usuario
            return render_template('chat.html',value=usuario)
        elif(data['username']=="jorge" and data['password']=="mayna"):
            session[usuario] = usuario
            return render_template('chat.html',value=usuario)
        elif (data['username'] == "marcos" and data['password'] == "dias"):
            session[usuario] = usuario
            return render_template('chat.html',value=usuario)
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop(usuario, None)
    return render_template('login.html')
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()