from flask import Flask, request, redirect, Response, render_template
import json
from Extras import database, encoder

dicmes = {}
session = database.Session()

app = Flask(__name__)
app.secret_key = "You Will Never Guess"


@app.route('/static/<content>')
def display_template(content):
    return render_template(content)


@app.route('/', methods=['GET'])
# Crea la base de datos de mensajes
def set_messages():
    if dicmes == {}:
        message1 = database.Message(
            id=1, sendby='Pedro', receiveby='Pancho', message='Hola como estas?')
        message2 = database.Message(id=2, sendby='Pancho',
                                    receiveby='Pedro', message='Bien, gracias')
        session.add(message1)
        session.add(message2)
        session.commit()

        # Meter mensajes en el cache
        listin = session.query(database.Message)
        for i in listin:
            dicmes[i.id] = [i.sendby, i.receiveby, i.message]

    return redirect("/messages")


@app.route('/messages', methods=['GET'])
def get_messages():
    response = []
    for m in session.query(database.Message):
        response.append(m)
    return json.dumps(response, cls=encoder.AlchemyEncoder)


@app.route('/messages', methods=['POST'])
def create_message():
    c = request.get_json(silent=True)
    newmessage = json.loads(request.form["values"])
    if newmessage["id"] not in dicmes:
        message = database.Message(id=newmessage['id'], sendby=newmessage['sendby'],
                                   receiveby=newmessage['receiveby'], message=newmessage['message'])
        session.add(message)
        session.commit()

        for i in newmessage:
            dicmes[newmessage["id"]] = [newmessage['sendby'],
                                        newmessage['receiveby'], newmessage['message']]

        return 'Message created'
    return "The id is already in use"


@app.route('/messages/<id>', methods=['GET'])
def get_message(id):
    messagey = session.query(database.Message).filter(database.Message.id == id)
    for m in messagey:
        js = json.dumps(m, cls=encoder.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    etc = {"status": 404, "message": "Not Found"}
    return Response(etc, status=404, mimetype='application/json')


@app.route('/messages', methods=['DELETE'])
def remove_message():
    id = request.form["key"]
    message = session.query(database.Message).filter(database.Message.id == id)
    dicmes.pop(id, None)  # -----
    for m in message:
        session.delete(m)
    session.commit()
    return "DELETED"

    etc = {"status": 404, "message": "Not Found"}
    return Response(etc, status=404, mimetype='application/json')


@app.route('/messages', methods=['PUT'])
def update_message():
    id = request.form["key"]
    message = session.query(database.Message).filter(database.Message.id == id).first()

    if message == None:
        etc = {"status": 404, "message": "Not Found"}
        return Response(etc, status=404, mimetype='application/json')

    update = json.loads(request.form['values'])

    for key in update.keys():
        setattr(message, key, update[key])
        #message.key = update[key]

    return "MESSAGE UPDATED"


if __name__ == '__main__':
    app.run()
