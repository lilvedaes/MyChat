from flask import Flask, render_template, request,session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base= declarative_base()
class User(Base):
    __tablename__ ='users'
    id= Column(Integer,primary_key=True)
    name= Column(String(50))
    username=Column(String(50))
    password = Column(String(12))

app = Flask(__name__)
@app.route("/")
def main():
    return render_template('login.html')
@app.route('/login', methods = ['POST'])
def login():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sesion = Session()
    user1 = User(id=1, name='dc', username='dylan', password='castro')
    user2 = User(id=2, name='jm', username='jorge', password='mayna')
    user3 = User(id=3, name='md', username='marcos', password='dias')
    sesion.add(user1)
    sesion.add(user2)
    sesion.add(user3)
    sesion.commit()
    exist=False
    if request.method == 'POST':
        data = request.form
        for username, password in sesion.query(User.username, User.password):
            if username == data['username'] and password == data['password']:
                session[(data['username'])] = data['username']
                return render_template('chat.html', value=data['username'])
                exist=True
        if exist==False:
            return render_template('login.html')
@app.route("/logout" , methods = ['POST'])
def logout():
    data = request.form
    session.pop(data['id'],None)
    return render_template('login.html')
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()