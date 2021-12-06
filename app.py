from os.path import join, dirname

from flask import Flask

import firebase_admin
from firebase_admin import credentials

from src.excerpt import EXCERPT_API
from src.game import GAME_API
from src.result import RESULT_API
from src.speaker import SPEAKER_API
from src.user import USER_API
from src.view import VIEW_API


app = Flask(__name__)

app.register_blueprint(USER_API, url_prefix='/user')
app.register_blueprint(EXCERPT_API, url_prefix='/excerpt')
app.register_blueprint(GAME_API, url_prefix='/game')
app.register_blueprint(RESULT_API, url_prefix='/result')
app.register_blueprint(SPEAKER_API, url_prefix='/speaker')
app.register_blueprint(VIEW_API, url_prefix='/view')

cred = credentials.Certificate(join(dirname(dirname(__file__)), '/app/serviceAccountKey.json'))
firebase_admin.initialize_app(cred)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)
