from flask import Blueprint, request

from db_connection import get_db_connection
from src.authentication import require_token

SPEAKER_API = Blueprint('speaker_api', __name__)


@SPEAKER_API.route('/fetchAllSpeakerIds', methods=['GET'])
def fetch_all_speaker_ids():
    return _fetch_all_speaker_ids()


@require_token()
def _fetch_all_speaker_ids():
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT DISTINCT id
                    FROM speaker
                    '''
                )
                result_list = cursor.fetchall()
    return {
        'speakerList': [speaker[0] for speaker in result_list]
    }
