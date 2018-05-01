from flask import Flask, render_template, request, session, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "You Will Never Guess"

#Base de datos

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(id=1, name='admin', fullname='Administrator', password='admin')

user2 = User(id=2, name='bear', fullname='Kang Seulgi', password='seulbear')

user3 = User(id=3, name='bunny', fullname='Bae Irene', password='hyunnie')

user4 = User(id=4, name='hamster', fullname='Song Wendy', password='wannie')

user5 = User(id=5, name='turtle', fullname='Kim Yeri', password='yerimie')

user6 = User(id=6, name='duck', fullname='Choi Joy', password='wannie')


session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)
session.commit()

alldatabase = session.query(User)

@app.route("/")
def login_page():
    return render_template('HTML.html')

@app.route('/dologin/', methods = ['POST'])
def dologin():

    yeslogin = False

    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['passw']

        for x in alldatabase:
            if user == x.name and passw == x.password:
                yeslogin = True

        if yeslogin == True:
            return redirect('/ChatPage.html')
        else:
            return redirect('/')

@app.route("/ChatPage.html")
def chat_page():
    return render_template('ChatPage.html')


if __name__ == '__main__':
    app.run()
