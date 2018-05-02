from flask import Flask
from model import entities
from database import connector
from sqlalchemy import *




app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/setUsers')
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
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse;
        print("From DB")
    else:
        print("From Cache")

    users = cache[key];
    response = ""
    for user in users:
        response += user.name+";"+user.fullname
    return response

if __name__ == '__main__':
    app.run()
