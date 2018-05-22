# COMMENTS IN ENGLISH

from sqlalchemy import Column, Integer, String
from database import connector

# User database
class User(connector.Manager.Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    fullname=Column(String(50))
    password=Column(String(15))

# Message database
class Message(connector.Manager.Base):
    __tablename__='messages'
    id=Column(Integer,primary_key=True)
    message=Column(String(100))
    received_by=Column(String(50))
    sent_by=Column(String(50))
    date=Column(String(50))
    time=Column(String(50))
