from flask import Flask, render_template, request,flash,session,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sergio/PycharmProjects/sergio.carbone/database.db'

db = SQLAlchemy(app)

class User(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	usuario = db.Column(db.String(15), unique=True)
	password = db.Column(db.String(15))

#carlos = User( id=1, usuario="carlos",password="1234")
#db.session.add(carlos)
#db.session.commit()

		

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/dologin', methods=['POST'])
def dologin():
	error= None
	user = User.query.filter_by(usuario= request.form['usuario']).first()
	if user:
		if user.password == request.form['password']:
			return render_template('chats.html') 
		else:
			return render_template('login.html',error=error)	

      
@app.route('/doregister' ,methods=['POST'])
def doregister():
	print request
	if request.form['password'] == request.form['password2']:
		new_user = User(usuario= request.form['usuario'],password= request.form['password'] )
		db.session.add(new_user)
		db.session.commit()
		return redirect('/')
		#return render_template('login.html')
	else:
		return render_template('registro.html')


if __name__ == '__main__':
    app.run(debug=True)