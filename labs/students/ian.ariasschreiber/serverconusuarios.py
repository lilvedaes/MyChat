from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

Usuarios=[]
@app.route('/')
def main():
    return "Para registrar un Usuario añada '/registrar/' y luego el nombre de usuario que quiera registrar. Para ver la cantidad de usuarios registrados añada '/cantidad. Para ver los usuarios registrados añada /getUsuarios. "




@app.route('/registrar/<USUARIO>')
def registrar(USUARIO):
    if 'USUARIO' not in session:
        session['USUARIO'] = ''
    session['USUARIO'] = str(session['USUARIO']) + " " + str(USUARIO)
    Usuarios.append(str(USUARIO))
    return "El usuario " + USUARIO +" ha sido registrado"

@app.route('/getUsuarios')
def currentusers():
    return "Los usuarios registrados son: " + session['USUARIO']



@app.route('/cantidad')
def cantidad():
    cantidad = len(Usuarios)
    return "La cantidad de usuarios registrados son: " + str(cantidad)

if __name__ == '__main__':
    app.run()
