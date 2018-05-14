from flask import Flask, render_template, request, session, redirect, Response
import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

Base = declarative_base()
cache = {}


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(String(50))
    sender = Column(String(10))
    receiver = Column(String(10))


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

########

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)

##########

app = Flask(__name__)

@app.route('/setmessages')
def setMessages():
    message1 = Message(id=1, message='SLEEEP Peter', sender='Mantis', receiver='Peter')
    message2 = Message(id=2, message='You do me nothing woman', sender='Peter', receiver='Mantis')

    session.add(message1)
    session.add(message2)
    session.commit()
    return 'Created Messages'


@app.route('/messages', methods = ['GET'] )#Return messages
def  returnMessages():
    key = 'return messages'
    if key not in cache.keys():
        dbResponse = session.query(Message)
        cache[key] = dbResponse
        print("From DB")
    else:
        print("From Cache")

    messages = cache[key];
    response = []
    for message in messages:
        response.append(message)
    return json.dumps(response, cls=AlchemyEncoder)


@app.route('/messages', methods = ['POST'])#New message created
def createMessages():
    c = request.get_json(silent=True)
    print ("Lo que escribiste: ", c)
    message = Message(id=c['id'], message=c['message'], sender=c['sender'], receiver=c['receiver'])
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messages/<id>', methods = ['GET'])#returns single message
def getMessage(id):
    messages = session.query(Message).filter(Message.id == id)
    for message in messages:
        js =json.dumps(message, cls=AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    error={"status":404, "message":"Not Found"}
    return Response(error, status=404, mimetype='application/json')

@app.route('/messages/<id>', methods = ['DELETE'])#message deleted
def removeMessage(id):
    messages = session.query(Message).filter(Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return 'DELETED'

@app.route('/messages/<id>', methods = ['PUT'])#message updated
def updateMessage(id):
    removeMessage(id)
    createMessages()
    return 'Message Updated'



if __name__ =='__main__':
    app.run()
