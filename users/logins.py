from flask import Flask, session
app = Flask(__name__)
app.secret_key= 'you will never guess'
@app.route('/logear/<nombre>')
def logear(nombre):
    users=[]
    if 'logear' not in session:
        users = []
    users.append(nombre)
    for i in users:
        return(i+" ")


if __name__=='__main__':
    app.run()
