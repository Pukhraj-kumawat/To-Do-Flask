from flask import Flask,render_template,redirect,request,url_for
from dotenv import load_dotenv
import os
import jwt

app = Flask(__name__)
 

@app.route('/<id>')
def home(id):
    return render_template('home.html',data='Pukhraj')
 
print(os.environ.get('SECRET_KEY'))

if __name__ == '__main__':
    app.run(debug=True)