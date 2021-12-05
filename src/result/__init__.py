from flask import Blueprint, request

from src.authentication import require_token
from src.db_connection import get_db_connection
from src.game import get_player
from src.result import query

RESULT_API = Blueprint('result_api', __name__)


@RESULT_API.route('/store', methods=['POST'])
def store():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = get_player(parameters['gameId'])
                return _store(
                    cursor=cursor,
                    user_id=user_id,
                    parameters=parameters
                )


@require_token(check_user=True)
def _store(cursor, user_id, parameters):
    return query.store(
        game_id=parameters['gameId'],
        excerpt_counter=parameters['excerptCounter'],
        user_id=parameters['userId'],
        socio_cultural_coordinate=parameters['socioCulturalCoordinate'],
        socio_economic_coordinate=parameters['socioEconomicCoordinate'],
        distance=parameters['distance'],
        cursor=cursor
    )
