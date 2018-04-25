from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

@app.route('/set_user/<usuario>')
def set(usuario):
    if 'username' not in session:
        session['username'] = ''
    session['username'] = str(session['username']) + "   " + str(usuario)
    return "Usuario Registrado: " + usuario

@app.route('/number_user')
def num():
    n = 0
    for x in range(0, len(session['username'].split())):
        n += 1
    return "La cantidad de usarios registrados es: " + str(n)

@app.route('/view_user')
def view():
    return "Usuarios activos: " + session['username']


if __name__ == '__main__':
    app.run()
