from flask import Blueprint, request

from db_connection import get_db_connection
from src.authentication import require_token

RESULT_API = Blueprint('result_api', __name__)


@RESULT_API.route('/fetchResultsByGameId/<game_id>', methods=['GET'])
def fetch_results_by_game_id(game_id):
    return _fetch_results_by_game_id(game_id)


@require_token()
def _fetch_results_by_game_id(game_id):
    # TODO: Maybe should check that game_id belongs to current user.
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate,
                        distance
                    FROM result
                    WHERE game_id = %(game_id)s
                    ''',
                    {'game_id': game_id}
                )
                result_list = cursor.fetchall()
    return {
        'resultList': [
            {
                'gameId': result[0],
                'excerptCounter': result[1],
                'userId': result[2],
                'socioCulturalCoordinate': result[3],
                'socioEconomicCoordinate': result[4],
                'distance': result[5]
            }
            for result in result_list
        ]
    }


@RESULT_API.route('/store', methods=['POST'])
def store():
    parameters = request.get_json()
    return _store(
        game_id=parameters['gameId'],
        excerpt_counter=parameters['excerptCounter'],
        user_id=parameters['userId'],
        socio_cultural_coordinate=parameters['socioCulturalCoordinate'],
        socioEconomicCoordinate=parameters['socioEconomicCoordinate'],
        distance=parameters['distance']
    )


@require_token(check_user=True)
def _store(game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate, distance):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO result (
                        game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate,
                        distance
                    )
                    VALUES (
                        %(game_id)s, %(excerpt_counter)s, %(user_id)s, %(socio_cultural_coordinate)s,
                        %(socioEconomicCoordinate)s, %(distance)s
                    )
                    ''',
                    {
                        'game_id': game_id,
                        'excerpt_counter': excerpt_counter,
                        'user_id': user_id,
                        'socio_cultural_coordinate': socio_cultural_coordinate,
                        'socioEconomicCoordinate': socio_economic_coordinate,
                        'distance': distance
                    }
                )
    return {}
