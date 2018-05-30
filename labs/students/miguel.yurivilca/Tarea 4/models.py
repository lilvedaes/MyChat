from sqlalchemy import Column, Integer, String
from database import Base
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

from database import init_db


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))

    def __init__(self,username=None, password=None):
        self.username = username
        self.password = password


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