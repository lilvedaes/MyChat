# COMMENTS IN ENGLISH

from flask import Flask,render_template,session,request,jsonify,Response,redirect
from model import entities
from database import connector
import json 

app=Flask(__name__)
db=connector.Manager()
# Cache dictionary created
cache={}
engine=db.createEngine()
# Session started
session=db.getSession(engine)
# Users list created
users=session.query(entities.User)
# Messages list created
messages=session.query(entities.Message)

# Root page
@app.route('/')
def main():
    return render_template('login.html')

# Chat page
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Set users
@app.route('/setUsers')
def set_users():
    user1=entities.User(id=1,name='at',fullname='Alan Turing',password='admin')
    user2=entities.User(id=2,name='lt',fullname='Linus Torvalds',password='linus')
    user3=entities.User(id=3,name='sj',fullname='Steve Jobs',password='steve')
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
    return 'Created users'

# Set messages
@app.route('/setMessages')
def set_messages():
    message1=entities.Message(id=1,message='Alan, Have you seen "The Imitation Game"',received_by='Alan Turing',sent_by='Steve Jobs',date='13/05/18',time='12:00:00')
    message2=entities.Message(id=2,message='No, I have not',received_by='Steve Jobs',sent_by='Alan Turing',date='13/05/18',time='12:00:23')
    message3=entities.Message(id=3,message='Linux is better than MacOS',received_by='Steve Jobs',sent_by='Linus Torvalds',date='13/05/18',time='12:00:35')
    message4=entities.Message(id=4,message='I do not think so',received_by='Linus Torvalds',sent_by='Steve Jobs',date='13/05/18',time='12:01:12')
    session.add(message1)
    session.add(message2)
    session.add(message3)
    session.add(message4)
    session.commit()
    return 'Created messages'

# Validate Users
@app.route('/dologin', methods=['POST'])
def do_login():
    if request.method=='POST':
        data=request.form                
        for i in users:
            if i.name==data['username'] and i.password==data['password']:
                return redirect('/chat')
        return redirect('/')


# Get all users
@app.route('/users',methods=['GET'])
def get_all_users():
    key='getUsers'
    if key not in cache.keys():
        cache[key]=users;
        print("From DB")
    else:
        print("From Cache")
    
    users_list=cache[key];
    response=[]
    for i in users_list:
        response.append(i)
    return json.dumps(response, cls=connector.AlchemyEncoder)

# Get all messages
@app.route('/messages',methods=['GET'])
def get_all_messages():
    key='getMessages'
    if key not in cache.keys():
        cache[key]=messages;
        print("From DB")
    else:
        print("From Cache")
    
    messages_list=cache[key];
    response=[]
    for i in messages_list:
        response.append(i)
    return json.dumps(response,cls=connector.AlchemyEncoder)
   

# Create user
@app.route('/users',methods=['POST'])
def create_user():
    c=request.get_json(silent=True)
    print(c)
    user=entities.User(id=c["id"],name=c["name"],fullname=c["fullname"],password=c["password"])
    session.add(user)
    session.commit()
    return 'Created user'

# Create message
@app.route('/messages',methods=['POST'])
def create_message():
    c=request.get_json(silent=True)
    print(c)
    message=entities.Message(id=c["id"],message=c["message"],received_by=c["received_by"],sent_by=c["sent_by"],date=c["date"],time=c["time"])
    session.add(message)
    session.commit()
    return 'Created message'

# Get single user
@app.route('/users/<id>',methods=['GET'])
def get_single_user(id):
    user_single=users.filter(entities.User.id==id)
    for i in user_single:
        js=json.dumps(i,cls=connector.AlchemyEncoder)
        return Response(js,status=200,mimetype='application/json')
    message={"status": 404,"message": "Not Found"}
    return Response(message,status=404,mimetype='application/json')

# Get single message
@app.route('/messages/<id>',methods=['GET'])
def get_single_message(id):
    message_single=messages.filter(entities.Message.id==id)
    for i in message_single:
        js=json.dumps(i,cls=connector.AlchemyEncoder)
        return Response(js,status=200,mimetype='application/json')
    message={"status": 404,"message": "Not Found"}
    return Response(js,status=404,mimetype='application/json')

# Update user
@app.route('/users/<id>',methods=['PUT'])
def update_user(id):
    delete_user(id)
    create_user()
    return 'Updated user'
    
    """ update=request.get_json(silent=True)
    print(update)
    current=users.filter(entities.User.id==id) """
    
    """ for key in current.keys():
        if key in update.keys():
            current[key]=update[key]
 """
    """ current[0]["name"]=request.json["name"]
    current[0]["fullname"]=request.json["fullname"]
    current[0]["password"]=request.json["password"]
    session.add(current)
    session.commit() """
    """ delete_message(id)
    create_user()
    return 'Updated user'
     """

# Update message
@app.route('/messages/<id>',methods=['PUT'])
def update_message(id):
    delete_message(id)
    create_message()
    return 'Updated message'
    
# Delete user
@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    deleted_user=users.filter(entities.User.id==id)
    for i in deleted_user:
        session.delete(i)
    session.commit()
    return 'Deleted user'

# Delete message
@app.route('/messages/<id>',methods=['DELETE'])
def delete_message(id):
    deleted_message=messages.filter(entities.Message.id==id)
    for i in deleted_message:
        session.delete(i)
    session.commit()
    return 'Deleted message'

if __name__=='__main__':
    app.run()

