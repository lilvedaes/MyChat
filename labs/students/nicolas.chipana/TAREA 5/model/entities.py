from sqlalchemy import Column, Integer, String
from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

class Message(connector.Manager.Base):
    __tablename__= 'message'
    id = Column(Integer, primary_key=True)
    msg = Column(String(300))

