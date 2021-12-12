from flask import request

from __main__ import socketio, session_to_user, user_to_session

from flask_socketio import emit

from src.db_connection import get_db_connection
from src.game import get_players
from src.result import query


@socketio.on('result_store')
def store(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id, target_user_id = get_players(json['gameId'], cursor)
                if user_id != session_to_user[request.sid]:
                    return 'no-such-game'
                response = _store(
                    cursor=cursor,
                    parameters=json
                )
    try:
        target_user_sid = user_to_session[target_user_id]
        emit('result_stored', {'userId': user_id, 'distance': json['distance']}, broadcast=True, to=target_user_sid)
        emit('own_result_stored', {'targetUserId': target_user_id, 'distance': json['distance']})
    except KeyError:
        pass
    return response


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
