from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

#configuracion inicial
app = Flask(__name__)
#creadion de la db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/finaledb.db'
db = SQLAlchemy(app)

#los usuarios
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    fullname = db.Column(db.String(50))
    password = db.Column(db.String(12))

#para los mensajes
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sendby = db.Column(db.String(50))
    receiveby = db.Column(db.String(50))
    message = db.Column(db.String(50))

db.create_all()

#workspace boi

@app.before_first_request
def set_default_users():
    #si la db esta vacia
    if (User.query.all()==[]):
        #db.session.add es para crear entradas (filas) en la base de datos
        db.session.add(User(id=1, name="furn", fullname="furnace furnandez", password="furnboi"))
        db.session.add(User(id=2, name="pursh", fullname="Apursh furnandez", password="pursh1"))
        db.session.add(User(id=3, name="yiyi", fullname="Alessia furnandez", password="yi"))

        db.session.add(Message(id=1, sendby="furnas", receiveby="meee", message="te quiero"))
        db.session.add(Message(id=2, sendby="furnaaaaaaas", receiveby="alessia", message="te quieroo"))
        db.session.add(Message(id=3, sendby="furnace", receiveby="andrea", message="te quierooo"))

        #cada vez que haga algo en la db tengo que hacer commit
        db.session.commit()

# main page
@app.route("/")
def main():
    return render_template('login.html')

#chat.html y usersCRUD.html
@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#login validate
@app.route('/dologin', methods = ['POST'])
def login():
    validated = False
    userList = User.query.all()
    if request.method == 'POST':
        data = request.form # a multidict containing post data
        for x in userList:
            if str(data['username']) == x.name and str(data['password']) == x.password:
                validated = True

        if validated == True:
            return redirect('/static/chat.html')
        else:
            return redirect('/')

#El buen CRUD <3 de usuarios

@app.route("/users", methods=['GET'])
def getAllUsers():
    if request.method == "GET":

        userList = User.query.all()

        users = "["
        for x in userList:
            users+='{"id":'+str(x.id)+',"name":"'+str(x.name)+'","fullname":"'+str(x.fullname)+'","password":"'+str(x.password)+'"},'
        users = users[0:len(users)-1] #para borrar la ultima coma
        users += ']'

        return users

@app.route("/users/<id>", methods = ["GET"])
def getOneUser(id):
    if request.method == "GET":
        x = User.query.get(id) #devuelve el elemento que tiene ese id
        user_json = '[{"id":'+str(x.id)+',"name":"'+str(x.name)+'","fullname":"'+str(x.fullname)+'","password":"'+str(x.password)+'"}]'
        return user_json

@app.route("/users", methods = ["POST"])
def createNewUser():
    if request.method == "POST":
        tempUser = json.loads(request.form["values"]) #el json.loads para pasar el request form de string a json
        newUser = User(id=int(tempUser["id"]),name=tempUser["name"], fullname=tempUser["fullname"], password=tempUser["password"])

        #lo metemos a la db
        db.session.add(newUser)
        db.session.commit()

        return "Se ha añadido el usuario"

@app.route("/users", methods = ["PUT"])
def updateUser():
    if request.method == "PUT":
        id = int(request.form["key"])
        x = User.query.get(id)  # devuelve el elemento que tiene ese id
        lacolumnadic = json.loads(request.form["values"]) # {"columna":"nuevo valor}
        lacolumna = list(lacolumnadic.keys())[0] # "columna"

        #si el nombre de la columna es igual a tal atributo
        if lacolumna == "name":
            x.name = lacolumnadic[lacolumna]
        elif lacolumna == "fullname":
            x.fullname = lacolumnadic[lacolumna]
        elif lacolumna == "password":
            x.password = lacolumnadic[lacolumna]

        #actualizamos bd
        db.session.commit()

        return "Se ha hecho el put"

@app.route("/users", methods = ["DELETE"])
def deleteUser():
    if request.method == "DELETE":
        id = int(request.form["key"])
        x = User.query.get(id)  # devuelve el elemento que tiene ese id

        #lo sacamos de la db
        db.session.delete(x)
        db.session.commit()

        return "Se ha borrado el usuario"

#El buen CRUD <3 de mensajes

@app.route("/messages", methods=['GET'])
def getAllMessages():
    if request.method == "GET":

        messageList = Message.query.all()

        messages = "["
        for x in messageList:
            messages+='{"id":'+str(x.id)+',"sendby":"'+str(x.sendby)+'","receiveby":"'+str(x.receiveby)+'","message":"'+str(x.message)+'"},'
        messages = messages[0:len(messages)-1] #para borrar la ultima coma
        messages += ']'

        return messages

@app.route("/messages/<id>", methods = ["GET"])
def getOneMessage(id):
    if request.method == "GET":
        x = Message.query.get(id) #devuelve el elemento que tiene ese id
        message_json = '[{"id":'+str(x.id)+',"sendby":"'+str(x.sendby)+'","receiveby":"'+str(x.receiveby)+'","message":"'+str(x.message)+'"}]'
        return message_json

@app.route("/messages", methods = ["POST"])
def createNewMessage():
    if request.method == "POST":
        tempMessage = json.loads(request.form["values"]) #el json.loads para pasar el request form de string a json
        newMessage = Message(id=int(tempMessage["id"]),sendby=tempMessage["sendby"], receiveby=tempMessage["receiveby"], message=tempMessage["message"])

        #lo metemos a la db
        db.session.add(newMessage)
        db.session.commit()

        return "Se ha añadido el mensaje"

@app.route("/messages", methods = ["PUT"])
def updateMessage():
    if request.method == "PUT":
        id = int(request.form["key"])
        x = Message.query.get(id)  # devuelve el elemento que tiene ese id
        lacolumnadic = json.loads(request.form["values"]) # {"columna":"nuevo valor}
        lacolumna = list(lacolumnadic.keys())[0] # "columna"

        #si el nombre de la columna es igual a tal atributo
        if lacolumna == "sendby":
            x.sendby = lacolumnadic[lacolumna]
        elif lacolumna == "receiveby":
            x.receiveby = lacolumnadic[lacolumna]
        elif lacolumna == "message":
            x.message = lacolumnadic[lacolumna]

        #actualizamos bd
        db.session.commit()

        return "Se ha hecho el put de mensajes"

@app.route("/messages", methods = ["DELETE"])
def deleteMessage():
    if request.method == "DELETE":
        id = int(request.form["key"])
        x = Message.query.get(id)  # devuelve el elemento que tiene ese id

        #lo sacamos de la db
        db.session.delete(x)
        db.session.commit()

        return "Se ha borrado el mensaje"

if __name__ == '__main__':
    app.run()