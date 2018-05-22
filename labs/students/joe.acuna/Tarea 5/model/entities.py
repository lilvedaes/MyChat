from sqlalchemy import Column, Integer, String
from database import connector


class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))


class Mensaje(connector.Manager.Base):
    __tablename__ = 'mensajes'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200))
