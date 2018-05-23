from flask import Flask, render_template, request, session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = '101658'

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

user1 = User(id=1, name='joe', username='Joe08', password='123')
user2 = User(id=2, name='armando', username='Armando3', password='aR123')
session.add(user1)
session.add(user2)
session.commit()


@app.route("/login")
def login():

    return render_template('login.html')


@app.route("/dologin", methods=['POST'])
def dologin():
    if request.method == 'POST':
        data = request.form
        users = session.query(User)
        for usuario, contra in users:
            if data['usuario'] == usuario and data['pass'] == contra:
                return render_template('chat.html')
            else:
                return render_template('login.html')
"""""
@app.route('/getUsers')
def get_user():
    key ='getUsers'
    if key not in cache-keys():
        dbResponse = session.query(User)
        cache[key] = dbResponse;
        print("From DB")
    else:.
        print("From Cache")
    
    users = chache[Key];
    response = "" 
    for user in users:
        response += user.name+";"+user.username
    return response
"""""

if __name__ == "__main__":
    app.run()
