from flask import Flask, render_template, request
#Con esto importo el archivo entities de la carpeta model.
from model import entities
#Con esto puedo importar el archivo connector de la carpeta database.
from database import connector





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
        if user.name == data["username"] and user.password == data ["password"]:
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


@app.route('/getUsers')
def get_user():
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
    response = ""
    for user in users:
        response += user.name+";"+user.fullname
    return response

if __name__ == '__main__':
    app.run()
