from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key="12345678"
online=[]

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        if "useronline" not in session:
            session ['useronline']=0
        usuario=request.form['usuario']
        contrasena= request.form['contraseña']
        if usuario == "USUARIO" and contrasena=="CONTRASEÑA":
            return redirect('/chat')
        elif usuario not in online and contrasena=="123":
            online.append(usuario)
            session['useronline']+=1
            return "Usuarios en linea: "+str(session['useronline'])+"<br> Usuarios en linea: </br>"+"".join(x+"<br>"for x in online)
        else:
            return redirect('/')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run()
