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
    return render_template('login2.html')

@app.route('/dologin',  methods = ['POST'])
def do_login():

    data = request.form
    session = db.getSession(engine)
    users = session.query(entities.User)
    for user in users:
        if user.name == data['Username'] and user.password == data['Password']:
            return render_template('chat.html')
    return render_template('login2.html')


@app.route('/message', methods = ['GET'])
def return_Message():
    session = db.getSession(engine)
    message = session.query(entities.Message)
    message_array = []
    for mess in message:
        message_array.append(mess)
    return json.dumps(message_array, cls=connector.AlchemyEncoder)

@app.route('/message/<id>', methods = ['GET'])
def get_Message(id):
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id)
    for mess in message:
        js = json.dumps(mess, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')

@app.route('/message/<id>', methods=['PUT'])
def update_Message(id):
    remove_Message(id)
    create_Menssage()
    return "Message Updated"

@app.route('/message/<id>', methods = ['DELETE'])
def remove_Message(id):
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id)
    for mess in message:
        session.delete(message)
    session.commit()
    return "MESSAGE DELETED"


@app.route('/message/create_message', methods = ['POST'])
def create_message():
    c = request.get_json(silent=True)
    print(c)
    mess = entities.Message(
        id=c['id'],
        content=c['new message']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'



if __name__ == '__main__':
    app.run()
