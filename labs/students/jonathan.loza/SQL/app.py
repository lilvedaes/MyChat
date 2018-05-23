from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, session, request, render_template

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))


engine=create_engine('sqlite:///:memory:',echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(id=1, name='ed', fullname='Ed Jones', password='hola123')
user2 = User(id=2, name='jb', fullname='Je Belli', password='bye123')
user3 = User(id=3, name='xd', fullname='Xavier Dias', password='bye123')
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

app=Flask(__name__)
app.secret_key= 'I dont know'

@app.route('/')
def login():
    return render_template("login.html")


@app.route('/dologin', methods=['POST'])
def dologin():
    if request.method == 'POST':
        data=request.form
        for usuario, contra in session.query(User.name, User.password):
            if usuario==data['usuario'] and contra==data['contraseña']:
                return render_template('chat.html')
            else:
                print('Usuario o contraseña incorrectos')
                return render_template('login.html')


if __name__=='__main__':
    app.run(port=8000)
