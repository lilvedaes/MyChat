from flask import Flask, render_template, session, request, jsonify, Response
from model import entities
from database import connector
import json


app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/dologin', methods=['POST'])
def do_login():

    data = request.form
    session = db.getSession(engine)
    users = session.query(entities.User)
    for user in users:
        if user.name == data['usuario'] and user.password == data['pass']:
            return render_template('chat.html')
    return render_template('login.html')


@app.route('/setUsers')
def set_user():

    user1 = entities.User(id=1, name='Joe08', fullname='Joe Acuña', password='hi123')
    user2 = entities.User(id=2, name='jb12', fullname='Je Belli', password='bye123')
    session = db.getSession(engine)
    session.add(user1)
    session.add(user2)
    session.commit()
    return 'Created users'


@app.route('/users', methods=['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    users = cache[key]
    response = []
    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    message = {"status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users/<id>', methods=['DELETE'])
def remove_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
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

"""Mensajes"""


@app.route('/mensajes', methods=['POST'])
def crearMensaje():
    c = request.get_json(silent=True)
    print(c)
    mensaje = entities.Mensaje(
        id=c['id'],
        contenido=c['contenido']
    )
    session = db.getSession(engine)
    session.add(mensaje)
    session.commit()
    return 'Mensaje creado'


@app.route('/mensajes', methods=['GET'])
def returnMensaje():
    session = db.getSession(engine)
    mensajes = session.query(entities.Mensaje)
    m_array = []
    for m in mensajes:
        m_array.append(m)
    return json.dumps(m_array, cls=connector.AlchemyEncoder)


@app.route('/messages/<id>', methods=['GET'])
def getMensaje(id):
    session = db.getSession(engine)
    message = session.query(entities.Mensaje).filter(entities.Mensaje.id == id)
    for men in message:
        js = json.dumps(men, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')
    message = {"status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')



@app.route('/mensaje/<id>', methods=['DELETE'])
def removerMensaje(id):
    session = db.getSession(engine)
    mensajes = session.query(entities.Mensaje).filter(entities.Mensaje.id == id)
    for mensaje in mensajes:
        session.delete(mensaje)
    session.commit()
    return "Mensaje eliminado"


@app.route('/mensaje/<id>', methods=['PUT'])
def updateMensaje(id):
    removerMensaje(id)
    crearMensaje()
    return "Mensaje actualizado"


if __name__ == '__main__':
    app.run()
