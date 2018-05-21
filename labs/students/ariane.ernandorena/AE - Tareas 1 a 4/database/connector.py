from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        #Especificamos donde se creará la base de datos.
        engine = create_engine("sqlite:///C:\\Users\\arian\\Documents\\UTEC\\Desarrollo Basado en Plataformas\\base.db", echo=True)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session
