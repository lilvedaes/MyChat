# Aquí pongo la entidad usuario, y creo la clase usuario

from sqlalchemy import Column, Integer, String, DateTime
from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

class Message(connector.Manager.Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    recipient = Column(String(50))
    sender = Column(String(50))




