from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        engine = create_engine('sqlite:///users.db', echo = True)
        self.Base.metadata.create_all(engine)

        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session