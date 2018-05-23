from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key ='Secret Password'

Base = declarative_base()
class User(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True)
   name = Column(String(50))
   username = Column(String(50))
   password = Column(String(12))

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(id=1, name='bd', username='bryandiaz', password='alumnocs123')
user2 = User(id=2, name='jb', username='jesusbellido', password='profecs123')
user3 = User(id=3, name='ec', username='ernestocuadros', password='profe2cs123')
session.add(user1)
session.add(user2)
session.add(user3)

session.commit()

@app.route("/")
def login():
    return render_template('login2.html')

@app.route("/dologin/", methods = ['POST'])
def dologin():
    if request.method == 'POST':
        data = request.form
        for username, password in session.query(User.username, User.password).all():
            if username == data['username'] and password == data['password']:
                return render_template('chat.html')
            else:
                return render_template('login2.html')

@app.route("/logout/", methods = ['POST'])
def logout():
    if request.method == 'POST':
        data = request.form
    session.pop(data["name1"], None)
    return render_template('login2.html')

if __name__== "__main__":
    app.run()
