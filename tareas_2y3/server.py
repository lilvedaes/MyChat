from flask import Flask, render_template, send_from_directory, session, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

users = {}

@app.route("/login", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form['usr_email']
        password = request.form['usr_password']

        if username not in users:
            users[username] = password
            return "Nuevo registro completado"
        else:
            if password != users[username]:
                return "Credenciales incorrectas"
            else:
                return "Usuarios: " + str(users) + "<br>Numero de usuarios registrados: " + str(len(users))



if __name__ == "__main__":
    app.run()

