from flask import Flask, render_template, session, request, redirect

app = Flask(__name__)
app.secret_key = '1'

@app.route('/')
def main():
	return redirect('/login')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_success')
def register_success():
    return render_template('register_success.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')




@app.route('/cuantas_letras/<nombre>')
def cuantas_letras(nombre):
    return render_template('/chat#' + nombre)

@app.route('/suma/<numero>')
def suma(numero):
    if 'suma' not in session:
        session['suma'] = 0

    session['suma'] = session['suma'] + int(numero)

    return str(session['suma'])


@app.route('/dologin', methods = ['POST'])
def dologin():
    if request.method != 'POST':
        return render_template('login.html', error = 1)

    data = request.form
    usr = '@' + data['username']
    pw = data['password']

    if usr not in session:
        return render_template('login.html', error = 2)

    if session[usr] != pw:
        return render_template('login.html', error = 3)

    return redirect('/chat')


@app.route('/doregister/', methods = ['POST'])
def doregister():
    if request.method != 'POST':
        return render_template('register.html', error = 1)

    data = request.form

    usr = '@' + data['username']
    pw = data['password']
    pwc = data['passwordconfirm']

    if usr == '' or pw == '' or pwc == '':
        return render_template('register.html', error = 2)

    if usr in session:
        return render_template('register.html', error = 3)

    if pw != pwc:
        return render_template('register.html', error = 4)

    session[usr] = pw


    if 'users' not in session:
        session['users'] = 0

    session['users'] += 1

    return redirect('/register_success')

if __name__ == '__main__':
	app.run(debug = True)