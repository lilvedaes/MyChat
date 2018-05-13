from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
dicmes = {}


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sendby = Column(String(50))
    receiveby = Column(String(50))
    message = Column(String(50))


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
