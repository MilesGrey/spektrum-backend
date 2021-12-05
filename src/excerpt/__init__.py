from flask import Blueprint, request

from src.authentication import require_token
from src.excerpt import query

EXCERPT_API = Blueprint('excerpt_api', __name__)


@EXCERPT_API.route('/report', methods=['POST'])
@require_token()
def report():
    parameters = request.get_json()
    return query.report(
        speech_id=parameters['speechId'],
        fragment=parameters['fragment']
    )
