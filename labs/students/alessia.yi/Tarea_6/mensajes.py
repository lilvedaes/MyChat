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
app.secret_key = "You Will Never Guess"
Base = declarative_base()

mensaje = {}


class Msg(Base):
    __tablename__ = 'mensajes'
    id = Column(Integer, primary_key=True)
    mensaje = Column(String(50))
    sendby = Column(String(50))
    receiveby = Column(String(50))

engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
lista = []

# Del prof -------------------------------------------------------------------------------------


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

#-----------------------------------------------------------------------------------------------


def getmensajes():

    if not lista: #Si la lista esta vacia
        mensaje1 = Msg(id=1, mensaje="Soy Manan", sendby="Manan", receiveby="Fefi")
        mensaje2 = Msg(id=2, mensaje="Yo soy Fefi", sendby="Fefi", receiveby="Manan")
        mensaje3 = Msg(id=3, mensaje="Soy un manati", sendby="Manan", receiveby="Fefi")
        mensaje4 = Msg(id=4, mensaje="Soy un oso", sendby="Fefi", receiveby="Manan")
        mensaje5 = Msg(id=5, mensaje="Ye", sendby="Manan", receiveby="Fefi")

        mensajes = [mensaje1, mensaje2, mensaje3, mensaje4, mensaje5]

        for x in mensajes:
            session.add(x)

        session.commit()

        var = session.query(Msg)

        for x in var:
            lista.append(x)

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/mensaje')
def verMensajes():
    getmensajes()

    return json.dumps(lista, cls=AlchemyEncoder)


@app.route('/mensaje', methods=['POST'])
def crearMensaje():
    c = json.loads(request.form['values'])
    print(c)
    mm = Msg(id=c['id'], mensaje=c['mensaje'], sendby=c['sendby'], receiveby=c['receiveby'])

    session.add(mm)
    session.commit()
    lista.append(mm)

    return 'Message created'


@app.route('/mensaje/<id>', methods=['GET'])
def getMensaje(id):

    mensaje = session.query(Msg).filter(Msg.id == id)

    for x in mensaje:
        js = (json.dumps(x, cls=AlchemyEncoder))
        return Response(js, status=200, mimetype='application/json')

    mm = {"status": 404, "message": "Not Found"}
    return Response(mm, status=404, mimetype='application/json')


@app.route('/mensaje', methods=['DELETE'])
def deleteMensaje():
    id = request.form['key']
    mensajes = session.query(Msg).filter(Msg.id == id)
    print("--------------------------------- ANTES LA LISTA ERA:", lista)

    for x in mensajes:
        session.delete(x)
        lista.remove(x)

    print("--------------------------------- AHORA LA LISTA ES:", lista)


    session.commit()

    return "Delete"


@app.route('/mensaje', methods=['PUT'])
def updateMensaje():
    id = request.form['key']
    mm = session.query(Msg).filter(Msg.id == id).first()
    c = json.loads(request.form['values'])

    for key in c.keys():
        setattr(mm, key, c[key])
    session.add(mm)
    session.commit()
    return 'Updated User'


if __name__ == '__main__':
    app.run()