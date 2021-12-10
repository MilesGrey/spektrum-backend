import os

from flask import Flask, request

from flask_socketio import SocketIO

import firebase_admin
from firebase_admin import credentials

from src.authentication import authenticate_user, AuthenticationError


app = Flask(__name__)

account_info = {
  'type': os.getenv('TYPE'),
  'project_id': os.getenv('PROJECT_ID'),
  'private_key_id': os.getenv('PRIVATE_KEY_ID'),
  'private_key': os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
  'client_email': os.getenv('CLIENT_EMAIL'),
  'client_id': os.getenv('CLIENT_ID'),
  'auth_uri': os.getenv('AUTH_URI'),
  'token_uri': os.getenv('TOKEN_URI'),
  'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
  'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL')
}

cred = credentials.Certificate(account_info)
firebase_admin.initialize_app(cred)

socketio = SocketIO(app, logger=True, engineio_logger=True)

user_to_session = {}
session_to_user = {}


@socketio.on('connect')
def connect(data):
    try:
        user_id = authenticate_user(data['auth']['token'])
        user_to_session[user_id] = request.sid
        session_to_user[request.sid] = user_id
        print(f'{user_id} connected!')
        return True
    except AuthenticationError:
        return False


@socketio.on('disconnect')
def disconnect():
    user_id = session_to_user.pop(request.sid)
    user_to_session.pop(user_id)
    print(f'{user_id} disconnected!')



from src import view
from src import user
from src import result
from src import game
from src import excerpt


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 80)
