from typing import List, Any

from flask import Flask, render_template, request, Response
#Con esto importo el archivo entities de la carpeta model.
from model import entities
#Con esto puedo importar el archivo connector de la carpeta database.
from database import connector
import json

app = Flask(__name__)

#Aquí estoy creando un objeto de la clase manager del archivo connector,
#que está creando la base de datos "db"
db = connector.Manager()


cache = {}  #Creo un diccionario para mi cache.
engine = db.createEngine() #Motor de base de datos.

@app.route('/') #El paréntesis me indica a qué directorio de la URL estoy yendo.
def hello_world():
    return render_template('login.html') #Me va a mostrar lo que dice el html de login.

@app.route('/dologin', methods = ['POST']) #Aquí mostraremos lo que pasa una vez que hacemos clic en Login, porque me lleva a esta dirección.
def do_login():
    data = request.form
    #viene de mi variable que se llama db, que viene del archivo connector
    session = db.getSession(engine)
    users = session.query(entities.User)
    #Creo una lista con los datos de la database. esto viene de entities.py
    for user in users:
        if user.name == data["username"] and user.password == data["password"]:
            return render_template("index.html")
    return render_template("login.html")

@app.route('/setUsers')
#La función set_user agrega los usuarios a la database.
def set_user():
    user1 = entities.User(id=1, name='ed', fullname='Ed Jones', password='hola123')
    user2 = entities.User(id=2, name='jb', fullname='Je Belli', password='bye123')
    session = db.getSession(engine)
    session.add(user1)
    session.add(user2)
    session.commit()

    return 'Created users'

@app.route('/users', methods=['GET'])
def get_users():
    key = 'getUsers'

    if key not in cache.keys():
        #Si no está en la cache, lo buscaremos en la database.
        session = db.getSession(engine) #Abre una sesion en la db
        dbResponse = session.query(entities.User) #Busca todos los usuarios.
        #Y además, lo agregaremos al cache.
        cache[key] = dbResponse;
        print("From DB")
    else:
        #Si está, imprimimos que esa información viene del cache.
        print("From Cache")

    users = cache[key];
    #Creamos una lista de usuarios que viene del cache.
    response = []
    #Creamos una lista a la cual anexaremos la respuesta con json.

    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)

@app.route('/users/<id>', methods=['GET'])
def get_user(id): #esto servirá para obtener solo UN usuario.
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    #seleccionamos al usuario con el id indicada,
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return Response (js, status=200, mimetype='application/json')

    message = {"status": 404, "message":"Not Found"}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def remove_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id ==id)
    for user in users:
        session.delete(user)
    session.commit()
    return "DELETED"

@app.route('/users', methods=['POST'])
def create_user():
    c = request.get_json(silent=True)
    print(c)
    user = entities.User(
        id=c['id'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created users'

@app.route('/users', methods=['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

#Vamos con las funciones y app routes para los mensajes...

@app.route('/messages', methods=['GET'])
#Returns all messages.
def get_messages():
    key = 'getMessages'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.Message)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    messages = cache[key]
    response = []
    for message in messages:
        response.append(message)
    return json.dumps(response, cls=connector.AlchemyEncoder)

@app.route('messages', methods=['POST'])
#Creates a new message.
def create_message():
    c = request.get_json(silent=True)
    print(c)
    message = entities.Message(
        id=c['id'],
        datetime=c['datetime'],
        recipient=c['recipient'],
        sender=c['sender']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messages/<id>', methods=['GET'])
#Gets a particular message.
def get_message(id):
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')
    message = {"status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')

@app.route('/messages/<id>', methods=['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/messages/<id>', methods=['DELETE'])
def remove_message(id):
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return 'DELETED MESSAGE'



if __name__ == '__main__':
    app.run()
