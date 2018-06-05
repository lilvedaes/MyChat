#para que se actualizen los archivos en el navegador tienes que hacer un cache refresh (control and click reload)

from flask import Flask, render_template, session, request, redirect

app = Flask(__name__) #, static_url_path='/static')
@app.route("/")
def main():
    return render_template('login.html')

@app.route('/dologin/', methods = ['POST'])
def login():
    if request.method == 'POST':
        data = request.form # a multidict containing post data
        print(data['username'])
        print(data['password'])
        if data['username'] == 'Admin' and data['password'] == 'Admin1':
            return redirect('/chat.html')
        else :
            return redirect('/')

@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
