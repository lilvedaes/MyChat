#para que se actualizen los archivos en el navegador tienes que hacer un cache refresh (control and click reload)

from flask import Flask, render_template, session, request, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__) #, static_url_path='/static')
app.secret_key = 'You will never guess'

userlist = []

Base = declarative_base()
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

@app.route("/")
def main():
    return render_template('login.html')

@app.route('/dologin/', methods = ['POST'])
def login():
    if 'suma' not in session:
        print('suma igualar a 0')
        session['suma'] = "0"

    if request.method == 'POST':
        data = request.form # a multidict containing post data
        print(data['username'])
        print(data['password'])

        if data['username'] == 'Admin' and data['password'] == 'Admin1':
            return redirect('/chat.html')
        elif data['username'] != 'Admin' and data['password'] == 'Admin1':
            if str(data['username']) not in userlist:
                userlist.append(str(data['username']))
                print('setuserlist', userlist)

                print('sumando 1')
                session['suma'] = int(session['suma']) + 1
            return redirect('/counter')
        else :
            return redirect('/')

@app.route('/counter')
def counterpage():
    return "The number of online users is: " + str(session['suma'])

@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')

@app.route('/getusers')
def getdem():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(id=1, name='ed', fullname='Ed Jones', password='hola123')
    user2 = User(id=2, name='jb', fullname = 'Je Belli', password = 'bye123')

    session.add(user1)
    session.add(user2)
    session.commit()
    print("holiwis", session.query(User))
    var = session.query(User)
    rpta = ""
    for x in var:
        rpta += x.name

    return rpta


if __name__ == '__main__':
    app.run()
