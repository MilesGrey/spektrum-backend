from os.path import join, dirname

from flask import Flask

import firebase_admin
from firebase_admin import credentials

from src.excerpt import EXCERPT_API
from src.game import GAME_API
from src.result import RESULT_API
from src.speaker import SPEAKER_API
from src.user import USER_API


app = Flask(__name__)

app.register_blueprint(USER_API, url_prefix='/user')
app.register_blueprint(EXCERPT_API, url_prefix='/excerpt')
app.register_blueprint(GAME_API, url_prefix='/game')
app.register_blueprint(RESULT_API, url_prefix='/result')
app.register_blueprint(SPEAKER_API, url_prefix='/speaker')

cred = credentials.Certificate(join(dirname(dirname(__file__)), 'serviceAccountKey.json'))
firebase_admin.initialize_app(cred)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
