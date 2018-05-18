from flask import Flask,render_template,session,request, jsonify, Response
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

@app.route('/dologin',  methods = ['POST'])
def do_login():

    data = request.form
    session = db.getSession(engine)
    users = session.query(entities.User)
    for user in users:
        if user.name == data['usuario'] and user.password == data['password']:
            return render_template('chat.html')
    return render_template('login.html')

@app.route('/setUsers')
def set_user():

    user1 = entities.User(id=3, name='ed', fullname='Ed Jones', password='hola123')
    user2 = entities.User(id=4, name='jb', fullname='Je Belli', password='bye123')
    session = db.getSession(engine)
    session.add(user1)
    session.add(user2)
    session.commit()
    return 'Created users'


@app.route('/users', methods = ['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse;
        print("From DB")
    else:
        print("From Cache")

    users = cache[key];
    response = []
    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users/<id>', methods = ['DELETE'])
def remove_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "DELETED"



@app.route('/users', methods = ['POST'])
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



@app.route('/setMessages')
def set_msj():

    mensaje1 = entities.Msj(id=3, mensaje='hola nena')
    mensaje2 = entities.Msj(id=4, mensaje='hola amigos')
    session = db.getSession(engine)
    session.add(mensaje1)
    session.add(mensaje2)
    session.commit()
    return 'Created messages'


@app.route('/messages', methods = ['GET'])
def return_msjs():
    session = db.getSession(engine)
    mensajes = session.query(entities.Msj)
    msjs = []
    for m in mensajes:
        msjs.append(m)
    return json.dumps(msjs, cls=connector.AlchemyEncoder)

@app.route('/messages', methods = ['POST'])
def create_msj():
    c = request.get_json(silent=True)
    print(c)
    msj = entities.Msj(
        id=c['id'],
        mensaje=c['name'],
    )
    session = db.getSession(engine)
    session.add(msj)
    session.commit()
    return 'Created message'


@app.route('/message/<id>', methods = ['GET'])
def get_msj(id):
    session = db.getSession(engine)
    msjs = session.query(entities.Msj).filter(entities.Msj.id == id)
    for m in msjs:
        js = json.dumps(m, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/messages/<id>', methods = ['DELETE'])
def remove_msj(id):
    session = db.getSession(engine)
    msjs = session.query(entities.Msj).filter(entities.Msj.id == id)
    for m in msjs:
        session.delete(m)
    session.commit()
    return "DELETED"



if __name__ == '__main__':
    app.run()
