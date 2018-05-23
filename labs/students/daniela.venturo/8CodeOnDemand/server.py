#para que se actualizen los archivos en el navegador tienes que hacer un cache refresh (control and click reload)

from flask import Flask, session, escape, request, render_template, redirect, Response, url_for
import json
from database import connector
from model import entities

app = Flask(__name__)
app.secret_key = 'You will never guess'

#create database
db = connector.Manager()
engine = db.createEngine()

@app.before_first_request
def set_default_users():
    danisession = db.getSession(engine)
    #chequear que es la primera vez creando database
    if(danisession.query(entities.User).first() is None):
        #creando usuarios
        user1 = entities.User(id=1, name='ed', fullname='Ed Jones', password='hola123')
        user2 = entities.User(id=2, name='yi', fullname = 'Yi Sato', password = 'friedchicken')
        user3 = entities.User(id=3, name='pursh', fullname = 'Arturo Cuya', password = 'pursh')
        user4 = entities.User(id=4, name='hey', fullname = 'heihei', password = 'boats')
        user5 = entities.User(id=5, name='furn', fullname = 'Furnace Fernandez', password = 'furnboi')
        user6 = entities.User(id=6, name='andreav', fullname = 'Andrea Velasquez', password = 'cuaccuac')

        #metiendo usuarios a la db
        danisession.add(user1)
        danisession.add(user2)
        danisession.add(user3)
        danisession.add(user4)
        danisession.add(user5)
        danisession.add(user6)

        #creando mensajes
        message1 = entities.Message(id=1, message='Hello, my name is Elder Price', sendby='Price', receiveby='Green')
        message2 = entities.Message(id=2, message='And I would like to share with you the most amazing book', sendby='Price', receiveby='Green')

        #metiendolos a la base de datos
        danisession.add(message1)
        danisession.add(message2)

        #hacemos el commit
        danisession.commit()
    return redirect('/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    danisession = db.getSession(engine)
    danisession.remove()

#creando diccionario cache
cache = {}

#main page
@app.route("/")
def main():
    danisession = db.getSession(engine)
    if 'username' in session:
        usuarioIN = danisession.query(entities.User).filter(entities.User.name == session['username']).first()
        usuarioIN.isactive = 1
        return render_template('chat.html')
    return render_template('login.html')

#chat.html y crud.html
@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#ACA EMPIEZAN LOS METODOS

#login validate
@app.route('/dologin', methods = ['GET', 'POST'])
def login():
    danisession = db.getSession(engine)
    if 'username' not in session:
        if request.method == "POST":
            if danisession.query(entities.User).filter(entities.User.name == request.form['username'], entities.User.password == request.form['password']).first() is not None:
                session['username'] = request.form['username']
                usuarioIN = danisession.query(entities.User).filter(entities.User.name == session['username']).first()
                print("Usuario conectado: ", usuarioIN)
                usuarioIN.isactive = 1
                danisession.commit()
                return redirect('/')
            else:
                return ('', 204)
        return render_template('login.html')
    return redirect('/')

@app.route('/logout')
def logout():
    danisession = db.getSession(engine)
    usuarioIN = danisession.query(entities.User).filter(entities.User.name == session['username']).first()
    usuarioIN.isactive = 0
    session.pop('username', None)
    danisession.commit()

    return redirect('/')

#get users cache
@app.route('/getusers')
def get_user():
    danisession = db.getSession(engine)
    key = 'getUsers'
    if key not in cache.keys():
        dbResponse = danisession.query(entities.User)
        cache[key] = dbResponse
        print("---------------------From DB")
    else:
        print("---------------------From cache")

    users = cache[key]
    response = ""
    for x in users:
        response += x.name + " " + x.fullname + "      "
    return response

#empezamos con los metodos de mensajes

#devuelve los mensajes de la db que tmb estan en el cache
@app.route('/messages', methods = ['GET'])
def returnMessages():
    key = 'return messages'
    if key not in cache.keys():
        danisession = db.getSession(engine)
        dbResponse = danisession.query(entities.Message)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    messages = cache[key]
    response = []
    for message in messages:
        response.append(message)
    return Response(json.dumps(response, cls=connector.AlchemyEncoder), mimetype='application/json')

#devuelve solo el mensaje que sale en el id
@app.route('/messages/<id>', methods = ['GET'])
def getMessage(id):
    danisession = db.getSession(engine)
    messages = danisession.query(entities.Message).filter(entities.Message.id == id) #solo los mensajes de este id
    for message in messages:
        js =json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    error={"status":404, "message":"Not Found"}
    return Response(error, status=404, mimetype='application/json')

#Crear un nuevo mensaje
@app.route('/messages', methods = ['POST'])
def createMessages():
    danisession = db.getSession(engine)
    c =  json.loads(request.form['values'])
    print ("c: ", c)
    message = entities.Message(id=c['id'],
                                message=c['message'],
                                sendby=c['sendby'],
                                receiveby=c['receiveby'])
    danisession.add(message)
    danisession.commit()
    return "Se ha creado el mensaje"

#borra el mensaje que indica el id
@app.route('/messages', methods = ['DELETE'])
def removeMessage():
    id = request.form['key']
    danisession = db.getSession(engine)
    messages = danisession.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        danisession.delete(message)
    danisession.commit()
    return "DELETED"

#actualiza el mensaje indicado por el id, primero lo deletea y despues se crea uno nuevo
@app.route('/messages', methods = ['PUT'])
def updateMessage():
    danisession = db.getSession(engine)
    id = request.form['key']
    message = danisession.query(entities.Message).filter(entities.Message.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    danisession.add(message)
    danisession.commit()
    return 'Se ha actualizado el mensaje'

if __name__ == '__main__':
    app.run()
