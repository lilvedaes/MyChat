from flask import Flask, render_template, send_from_directory, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/myDb.db'
base = declarative_base()

users = {}

class User(base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))


engine = create_engine('sqlite:////tmp/myDb.db', echo=True)
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

user_boi = User(username="boi", password="boboboi")
@app.route("/test")
def test():
    session.add(user_boi)
    session.commit()
    queried_users = session.query(User)

    for boi in queried_users:
        print(boi.id)
        print(boi.username)
        print(boi.password)

    return "done"


@app.route("/login", methods=["POST"])
def login():
    login_success = False
    if request.method == "POST":
        username = request.form['usr_email']
        password = request.form['usr_password']
        usr = User(username = username, password = password)
        query = session.query(User)
        queried_users = []

        for u in query:
            queried_users.append((u.username, u.password))

        print("Queried users:")
        for x in queried_users:
            print(x)

        if usr.username not in [x[0] for x in queried_users]:
            session.add(usr)
            session.commit()
            return "Nuevo registro completado"
        else:
            if usr.password not in [x[1] for x in queried_users]:
                return "Credenciales incorrectas"
            else:
                r = ""
                for u in queried_users:
                    r += str(u) + "<br>"
                return r

def load_users(user_list):
    users = ""
    for u in user_list:
        users += u.username + "<br>"

    users += "<br>Numero de usuarios: " + str(len(user_list))
    return users

if __name__ == "__main__":
    app.run()

