from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta
from database import connector
import json


#para los users
class User(connector.Manager.Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

#para los mensajes
class Message(connector.Manager.Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sendby = Column(String(50))
    receiveby = Column(String(50))
    message = Column(String(50))
