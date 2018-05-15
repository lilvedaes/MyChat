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
    sesion = db.getSession(engine)
    users = sesion.query(entities.User)
    for user in users:
        id_siguiente=int(user.id)+1
    print(id_siguiente)
    return render_template('login.html',value=id_siguiente)

@app.route('/dologin',  methods = ['POST'])
def do_login():

    data = request.form
    sesion = db.getSession(engine)
    users = sesion.query(entities.User)
    for user in users:
        if user.name == data['username'] and user.password == data['password']:
            session[str(user.id)] = data['username']
            return render_template('chat.html', value=user.name,id=user.id)
    return render_template('login.html')

@app.route('/setUsers')
def set_user():

    user1 = entities.User(id=3, name='dylan', fullname='castro zorrilla', password='castro')
    session = db.getSession(engine)
    session.add(user1)
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
    if request.method == 'DELETE':
        session = db.getSession(engine)
        users = session.query(entities.User).filter(entities.User.id == id)
        for user in users:
            session.delete(user)
        session.commit()
        session.pop(id, None)
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

@app.route("/logout" , methods = ['POST'])
def logout():
    data = request.form
    session.pop(data['id'],None)
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
