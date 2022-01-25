from flask import request
from flask_socketio import emit

from __main__ import socketio, session_to_user, user_to_session

from src.db_connection import get_db_connection
from src.game import query
from src.game.query import get_players, get_latest_game


@socketio.on('game_set_game_finished')
def set_game_finished(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id, target_user_id = get_players(json['gameId'], cursor)
                if user_id != session_to_user[request.sid]:
                    return 'no-such-game'
                response = _set_game_finished(
                    cursor=cursor,
                    game_id=json['gameId']
                )
                both_finished_game = get_latest_game(target_user_id, user_id, cursor)['isFinished']
    if both_finished_game:
        try:
            target_user_sid = user_to_session[target_user_id]
            emit('both_finished_game', {'userId': user_id}, broadcast=True, to=target_user_sid)
        except KeyError:
            print(f'{target_user_id} is not connected')
        try:
            user_sid = user_to_session[user_id]
            emit('both_finished_game', {'userId': target_user_id}, broadcast=True, to=user_sid)
        except KeyError:
            print(f'{user_id} is not connected')
    return response


def _set_game_finished(cursor, game_id):
    return query.set_game_finished(
        game_id=game_id,
        cursor=cursor
    )
