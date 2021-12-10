from flask import request

from __main__ import socketio, session_to_user

from src.db_connection import get_db_connection
from src.game import query
from src.game.query import get_player


@socketio.on('game_set_game_finished')
def set_game_finished(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = get_player(json['gameId'], cursor)
                if user_id != session_to_user[request.sid]:
                    return 'no-such-game'
                return _set_game_finished(
                    cursor=cursor,
                    game_id=json['gameId']
                )


def _set_game_finished(cursor, game_id):
    return query.set_game_finished(
        game_id=game_id,
        cursor=cursor
    )
