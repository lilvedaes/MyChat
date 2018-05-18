from flask import Flask, render_template, session, request
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

engine=create_engine('sqlite:///:memory:',echo= True)
Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session1=Session()

user1=User(id=1,name='ed',username='jorge',password='mayna')
user2=User(id=2,name='jb',username='dylan',password='castro')
user3=User(id=3,name='eb',username='elena',password='benel')
user4=User(id=4,name='ep',username='el pro',password='io')

session1.add(user1)
session1.add(user2)
session1.add(user3)
session1.add(user4)

session1.commit()

app = Flask(__name__)
app.secret_key = 'you will never guess'


@app.route("/")
def main():
    return render_template('login.html')




@app.route('/login', methods = ['POST'])
def login():
    global usuario
    if request.method == 'POST':
        data = request.form


        for usuario, password in session1.query(User.username, User.password):
            if usuario==data['username'] and password==data['password']:
                session[usuario]=usuario
                return render_template('chaat.html',nombre=usuario)

        return render_template('login.html')







@app.route('/logout',methods=['POST'])
def logout():
    if request.method == 'POST':
        data = request.form

    session.pop(data["nombre1"], None)
    return render_template('login.html')


if __name__ == "__main__":
    app.run()