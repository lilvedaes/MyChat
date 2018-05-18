import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tableini import *

engine = create_engine('sqlite:///data.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

user = User("Reynaldo", "Rojas")
session.add(user)

user = User("user1", "user2")
session.add(user)

user = User("abc", "123")
session.add(user)

session.commit()
