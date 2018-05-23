#para que se actualizen los archivos en el navegador tienes que hacer un cache refresh (control and click reload)

from flask import Flask, render_template, session, request, redirect, Response
import json
from database import connector
from model import entities

app = Flask(__name__) #, static_url_path='/static')
app.secret_key = 'You will never guess'

session = connector.Session()

#creando usuarios
user1 = connector.User(id=1, name='ed', fullname='Ed Jones', password='hola123')
user2 = connector.User(id=2, name='yi', fullname = 'Yi Sato', password = 'friedchicken')
user3 = connector.User(id=3, name='pursh', fullname = 'Arturo Cuya', password = 'pursh')
user4 = connector.User(id=4, name='hey', fullname = 'heihei', password = 'boats')
user5 = connector.User(id=5, name='furn', fullname = 'Furnace Fernandez', password = 'furnboi')
user6 = connector.User(id=6, name='andreav', fullname = 'Andrea Velasquez', password = 'cuaccuac')

#metiendo usuarios a la db
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)

#creando mensajes
message1 = connector.Message(id=1, message='Hello, my name is Elder Price', sendby='Price', receiveby='Green')
message2 = connector.Message(id=2, message='And I would like to share with you the most amazing book', sendby='Price', receiveby='Green')

#metiendolos a la base de datos
session.add(message1)
session.add(message2)

#hacemos el commit
session.commit()

#creando lista de usuarios
allusers = session.query(connector.User)

#creando diccionario cache
cache = {}

#main page
@app.route("/")
def main():
    return render_template('login.html')

#chat page
@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')

#ACA EMPIEZAN LOS METODOS

#login validate
@app.route('/dologin/', methods = ['POST'])
def login():
    validated = False
    if request.method == 'POST':
        data = request.form # a multidict containing post data
        for x in allusers:
            if str(data['username']) == x.name and str(data['password']) == x.password:
                validated = True

        if validated == True:
            return redirect('/chat.html')
        else:
            return redirect('/')

#get users cache
@app.route('/getusers')
def get_user():
    key = 'getUsers'
    if key not in cache.keys():
        dbResponse = session.query(connector.User)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From cache")

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
        dbResponse = session.query(connector.Message)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    messages = cache[key]
    response = []
    for message in messages:
        response.append(message)
    return json.dumps(response, cls=entities.AlchemyEncoder)

#devuelve solo el mensaje que sale en el id
@app.route('/messages/<id>', methods = ['GET'])
def getMessage(id):
    messages = session.query(connector.Message).filter(connector.Message.id == id) #solo los mensajes de este id
    for message in messages:
        js =json.dumps(message, cls=entities.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    error={"status":404, "message":"Not Found"}
    return Response(error, status=404, mimetype='application/json')

#Crear un nuevo mensaje
@app.route('/messages', methods = ['POST'])
def createMessages():
    c = request.get_json(silent=True)
    print ("c: ", c)
    message = connector.Message(id=c['id'],
                                message=c['message'],
                                sendby=c['sendby'],
                                receiveby=c['receiveby'])
    session.add(message)
    session.commit()
    return "Se ha creado el mensaje"

#borra el mensaje que indica el id
@app.route('/messages/<id>', methods = ['DELETE'])
def removeMessage(id):
    messages = session.query(connector.Message).filter(connector.Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "DELETED"

#actualiza el mensaje indicado por el id, primero lo deletea y despues se crea uno nuevo
@app.route('/messages/<id>', methods = ['PUT'])
def updateMessage(id):
    removeMessage(id)
    createMessages()
    return "Se ha actualizado el mensaje"

if __name__ == '__main__':
    app.run()
