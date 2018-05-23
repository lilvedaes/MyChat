from sqlalchemy import Column, String, Boolean
from database import connector

class User(connector.Manager.Base):
    __tablename__ = "users"
    id = Column(String, primary_key = True)
    username = Column(String)
    password = Column(String)
    online = Column(Boolean)

    def __init__(self, usr, pw):
        self.id = '@' + usr
        self.username = usr
        self.password = pw
        self.online = False