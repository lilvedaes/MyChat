from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

@app.route('/sumar/<numero>')
def sumar(numero):
      if 'suma' not in session:
          session['suma'] = "0"

      session['suma'] = int(session['suma']) + int(numero)
      return str(session['suma'])

if __name__ == '__main__':
     app.run()