from flask import Flask, render_template, request, redirect, Response
import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__)

Base = declarative_base()
app.secret_key = "You Will Never Guess"
message = {}

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(String(50))
    sender = Column(String(10))
    receiver = Column(String(10))


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
list = []

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

def getmessages():
    if not list:
        message1 = Messages(id=1, message='SLEEEP Peter', sender='Mantis', receiver='Peter')
        message2 = Messages(id=2, message='You do me nothing woman', sender='Peter', receiver='Mantis')

        messages = [message1, message2]

        for x in messages:
            session.add(x)
        session.commit()

        var = session.query(Messages)

        for x in var:
            list.append(x)

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/messages')#Return messages
def returnMessages():
    getmessages()
    return json.dumps(list, cls=AlchemyEncoder)


@app.route('/messages', methods=['POST'])#New message created
def createMessages():
    c = json.loads(request.form['values'])
    print(c)
    #c = request.get_json(silent=True)
    mm = Messages(
        id=c['id'],
        message=c['message'],
        sender=c['sender'],
        receiver=c['receiver']
    )
    session.add(mm)
    session.commit()
    list.append(mm)
    return 'Created Message'

@app.route('/messages/<id>', methods = ['GET'])#returns single message
def getMessage(id):
    message = session.query(Messages).filter(Messages.id == id)
    for x in message:
        js = json.dumps(x, cls=AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    error={"status": 404, "message":"Not Found"}
    return Response(error, status=404, mimetype='application/json')

@app.route('/messages', methods = ['DELETE'])#message deleted /<id>'
def removeMessage():
    id = request.form['key'] #New
    messages = session.query(Messages).filter(Messages.id == id)
    print("Antes la lista era: ", list)
    for x in messages:
        session.delete(x)
        list.remove(x)
    print("Ahora la lista es: ", list)
    session.commit()
    return 'DELETED'

@app.route('/messages', methods = ['PUT'])#message updated
def updateMessage():
    id = request.form['key']
    mm = session.query(Messages).filter(Messages.id == id).first()
    c = json.loads(request.form['values'])

    for key in c.keys():
        setattr(mm, key, c[key])
    session.add(mm)
    session.commit()

    return 'Updated User'



if __name__ =='__main__':
    app.run()