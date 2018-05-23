from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

#creacion de base de datos

Base = declarative_base()

#para los users
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

#para los mensajes
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sendby = Column(String(50))
    receiveby = Column(String(50))
    message = Column(String(50))

#creando db
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

#creando session
Session = sessionmaker(bind=engine)
session = Session()
