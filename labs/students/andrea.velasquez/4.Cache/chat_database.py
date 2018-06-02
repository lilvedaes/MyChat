import time
from flask import Flask, session, request, render_template, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#------------------------SQLAlchemy-----------------------------------------------------
Base = declarative_base()
dicusers = {}


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(12))
    fullname = Column(String(50))


#------------------------FLASK-----------------------------------------------------
app = Flask(__name__)
app.secret_key = "You Will Never Guess"


@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/dologin', methods=['POST', 'GET'])
def dologin():
    global dicusers
    if request.method == 'POST':
        getusers()
        user = request.form['user']
        passw = request.form['pass']

        if user in dicusers and passw == dicusers[user][0]:
            dicusers = {}
            return render_template('Chat.html')
        else:
            time.sleep(1)
            return redirect("/")


#@app.route('/getusers', methods=['POST', 'GET'])
def getusers():
    global dicusers
    if dicusers == {}:  # if empty
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        user1 = User(id=1, username='ironduck', password='capsucks', fullname='Tony Stark')
        user2 = User(id=2, username='capiduckmerica',
                     password='makeduckmericagreatagain', fullname='Steve Rogers')
        user3 = User(id=3, username='dulk', password='dulkSMASH', fullname='Bruce Banner')
        user4 = User(id=4, username='dhor', password='missmyhammer',
                     fullname='Thor, King of Ducksgard')
        user5 = User(id=5, username='duckwidow', password='rocketsmyex',
                     fullname='Natasha Romanoff')
        user6 = User(id=6, username='duckeye', password='strongestavenger', fullname='Clint Barton')

        session.add(user1)
        session.add(user2)
        session.add(user3)
        session.add(user4)
        session.add(user5)
        session.add(user6)
        session.commit()

        listin = session.query(User)

        for i in listin:
            dicusers[i.username] = [i.password, i.fullname]

        print("------------------------------FROM DATABASE---------------------------")

    else:
        print("------------------------------FROM CACHE---------------------------")

    return


if __name__ == '__main__':
    # dicusers = {}
    app.run()
