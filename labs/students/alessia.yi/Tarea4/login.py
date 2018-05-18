from flask import Flask, session, request, render_template, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "You Will Never Guess"
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dologin/', methods=['POST'])
def dologin():
    if request.method == 'POST':
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        users={}

        user1 = User(id=1, username='manan', fullname='Manati', password='rio')
        user2 = User(id=2, username='leo', fullname='Leon', password='selva')
        user3 = User(id=3, username='wally', fullname='Beluga', password='ozzeano')
        user4 = User(id=4, username='fefi', fullname='Oso', password='bosque')
        user5 = User(id=5, username='husky', fullname='Perro', password='nieve')

        usuarios = [user1, user2, user3, user4, user5]

        for x in usuarios:
            session.add(x)

        session.commit()

        var = session.query(User)

        for x in var:
            users[x.username]= x.password

        username= request.form['username']
        password= request.form ["password"]

        if username in users and password==users[username]:
            return redirect('/chat.html')
        else:
            return redirect('/')


@app.route('/chat.html')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
