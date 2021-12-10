from flask import request

from __main__ import socketio, session_to_user

from src.db_connection import get_db_connection
from src.game import get_player
from src.result import query


@socketio.on('result_store')
def store(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = get_player(json['gameId'], cursor)
                if user_id != session_to_user[request.sid]:
                    return 'no-such-game'
                return _store(
                    cursor=cursor,
                    parameters=json
                )


def _store(cursor, parameters):
    return query.store(
        game_id=parameters['gameId'],
        excerpt_counter=parameters['excerptCounter'],
        user_id=parameters['userId'],
        socio_cultural_coordinate=parameters['socioCulturalCoordinate'],
        socio_economic_coordinate=parameters['socioEconomicCoordinate'],
        distance=parameters['distance'],
        cursor=cursor
    )
