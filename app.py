from auth.auth import create_token,verify_token
from flask import Flask,render_template,redirect,request,url_for,session,jsonify,make_response
from dotenv import load_dotenv
import os,jwt
from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

payload = {'user_id': 1234, 'username': 'john_doe'}


client = MongoClient(os.environ.get('MONGODB_CONNECTION_STRING'))
db = client['test']
to_do_user = db['ToDoUser']
to_do_data = db['ToDoData']

@app.route('/login', methods=['GET'])
def login():  
    jwt_token = request.cookies.get('jwt_token')      
    if not jwt_token:
        response = make_response(render_template('login.html'))
        return response
    return 'Already logged in'

@app.route('/signUp',methods = ['GET'])        
def signUp(): 
    jwt_token = request.cookies.get('jwt_token')      
    if not jwt_token:  
        response = make_response(render_template('signUp.html'))
        return response
    return 'Already logged in'
 

@app.route('/signedUp',methods = ['POST'])
def signedUp():
    hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    if request.form.get('password') == request.form.get('confirm-password'):
        to_do_user.insert_one({
            "email":request.form.get('email'),
            "first_name":request.form.get('first-name'),
            "last_name":request.form.get('last-name'),
            "password":hashed_password
        })
        payload = {'email':request.form.get('email'),'password':hashed_password}        
        jwt_token = create_token(payload)
        response = make_response(render_template('home.html'))
        response.set_cookie('jwt_token', jwt_token, httponly=True, secure=True)    
        return response
    return 'Password not matched'

@app.route('/loggedIn',methods = ['POST'])
def loggedIn():
    email = request.form.get('email')
    hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    user = to_do_user.find_one({'email':email,'password':hashed_password})
    if user:
        payload = {'email':email,'password':hashed_password}        
        jwt_token = create_token(payload)
        response = make_response(render_template('home.html'))
        response.set_cookie('jwt_token', jwt_token, httponly=True, secure=True)    
        return response
    else:
        return 'User do not exist'


@app.route('/logout')
def logout():
    response = make_response('Logged out successfully!')    
    response.delete_cookie('jwt_token')    
    return response

@app.route('/')
def home():
    jwt_token = request.cookies.get('jwt_token')      
    if not jwt_token:        
        return redirect('/login')
    payload = verify_token(jwt_token)
    user = to_do_user.find_one({"email":payload["email"]})
    to_dos = to_do_data.find({"user":user["_id"]})
    response = make_response(render_template('home.html',todos = list(to_dos)))
    return response

@app.route('/add-toDo',methods=['POST'])
def add_toDo():
    todo = request.form.get('todo-input')
    payload = verify_token(request.cookies.get('jwt_token'))
    user = to_do_user.find_one({"email":payload["email"]})
    to_do_data.insert_one({"toDo":todo,"user":user["_id"]})    
    return redirect('/')


@app.route('/edit-toDo',methods=['POST'])
def edit_toDo():
    jwt_token = request.cookies.get('jwt_token')      
    if not jwt_token:        
        return redirect('/login')
    payload = verify_token(jwt_token)
    if payload:
        toDoObject = to_do_data.find({"_id":request.form.get('toDoId')})
        if toDoObject:     
            to_do_id = ObjectId(request.form.get('toDoId'))                                                       
            update_result = to_do_data.update_one({"_id": to_do_id}, {"$set": {"toDo": request.form.get('toDoInput')}})            
            if update_result.modified_count == 1:
                return redirect('/')
            else:
                return 'some error'

@app.route('/delete-toDo',methods = ['POST'])
def delete_toDo():
    jwt_token = request.cookies.get('jwt_token')      
    if not jwt_token:        
        return redirect('/login')
    payload = verify_token(jwt_token)
    if payload:
        toDoObject = to_do_data.find({"_id":request.form.get('toDoId')})
        if toDoObject:     
            to_do_id = ObjectId(request.form.get('toDoId')) 
            deleted_data = to_do_data.delete_one({"_id": to_do_id})
            if deleted_data.deleted_count == 1:
                return redirect('/')
            else:
                return 'some error'

        

if __name__ == '__main__':
    app.run(debug=True)