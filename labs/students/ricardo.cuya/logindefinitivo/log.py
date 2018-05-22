
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, session , request , render_template
app = Flask(__name__)
app.secret_key= 'Zun DA DA ZUN DADA ZUNZUN DADA'

Base = declarative_base()
class User(Base):
	__tablename__='users'
	id = Column(Integer,primary_key=True)
	name = Column(String(50))
	fullname=Column(String(50))
	password=Column(String(12))

engine=create_engine('sqlite:///:memory:' , echo=True)
Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()

user1= User(id=1, name='ed@gmail.com', fullname='Ed Jones', password='hola123')
user2= User(id=2, name='jb@gmail.com', fullname='Je Beli', password='bye123')
session.add(user1)
session.add(user2)
session.commit()

@app.route('/dologin',methods=['POST'])
def dologin():

    if request.method == 'POST':
        data=request.form
        for row in session.query(User.name, User.password).all():
            if data['username']==row.name and data['passwd']==row.password:
                return render_template('chat.html')
            else:
                continue
        return render_template('login.html')



@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')





if __name__ =='__main__':
    app.run()
