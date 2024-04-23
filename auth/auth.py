import jwt,os
from flask import Flask

app = Flask(__name__)

def create_token(payload):
    return jwt.encode(payload, os.environ.get('SECRET_KEY'),algorithms="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'),algorithms="HS256")
        return payload
    except Exception as e:
        print('Some error :',e)

    # except jwt.ExpiredSignatureError:
    #     return 'Signature expired. Please log in again.'
    # except jwt.InvalidTokenError:
    #     return 'Invalid token. Please log in again.'
