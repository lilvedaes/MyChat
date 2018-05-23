from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session