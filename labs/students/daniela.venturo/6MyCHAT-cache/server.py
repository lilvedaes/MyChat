#para que se actualizen los archivos en el navegador tienes que hacer un cache refresh (control and click reload)

from flask import Flask, render_template, session, request, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__) #, static_url_path='/static')
app.secret_key = 'You will never guess'

Base = declarative_base()
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

#creando usuarios
user1 = User(id=1, name='ed', fullname='Ed Jones', password='hola123')
user2 = User(id=2, name='yi', fullname = 'Yi Sato', password = 'friedchicken')
user3 = User(id=3, name='pursh', fullname = 'Arturo Cuya', password = 'pursh')
user4 = User(id=4, name='hey', fullname = 'heihei', password = 'boats')
user5 = User(id=5, name='furn', fullname = 'Furnace Fernandez', password = 'furnboi')
user6 = User(id=6, name='andreav', fullname = 'Andrea Velasquez', password = 'cuaccuac')

#creando db
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

#creando session
Session = sessionmaker(bind=engine)
session = Session()

#metiendo usuarios a la db
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)
session.commit()

#creando lista de usuarios
allusers = session.query(User)

#creando diccionario cache
cache = {}

@app.route("/")
def main():
    return render_template('login.html')

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

@app.route('/getusers')
def get_user():
    key = 'getUsers'
    if key not in cache.keys():
        dbResponse = session.query(User)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From cache")

    users = cache[key]
    response = ""
    for x in users:
        response += x.name + " " + x.fullname + "      "
    return response

@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
