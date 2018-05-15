from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)
app.secret_key = 'Codigo Secreto Incrackeable'

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

user1 = User(id=1, name='jbellido', fullname='Jesus Bellido', password='12345678')
user2 = User(id=2, name='chip', fullname='Nicolas Chipana', password='123')
session.add(user1)
session.add(user2)
session.commit()

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/dologin',methods=['POST'])
def dologin():
    if request.method == 'POST':
        data = request.form
        for usuario,password in session.query(User.name, User.password).all():
            if data['uname'] == usuario and data['pname'] == password:
                return render_template('Chat.html')
            else:
                return render_template('Login.html')


if __name__ == '__main__':
    app.run()
