from flask import Blueprint, request

from db_connection import get_db_connection
from src.authentication import require_token

GAME_API = Blueprint('game_api', __name__)


@GAME_API.route('/getGameId', methods=['POST'])
def get_game_id():
    parameters = request.get_json()
    return _get_game_id(
        user_id=parameters['loggedInPlayer'],
        other_player=parameters['otherPlayer']
    )


@require_token()
def _get_game_id(user_id, other_player):
    # TODO: Maybe check if current user belongs to the game.
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT id
                    FROM game
                    WHERE logged_in_player = %(logged_in_player)s
                    AND other_player = %(other_player)s
                    AND game_created = (
                    SELECT MAX(game_created)
                    FROM game
                    WHERE logged_in_player = %(logged_in_player)s
                    AND other_player = %(other_player)s 
                    )
                    ''',
                    {'logged_in_player': user_id, 'other_player': other_player}
                )
                game_id = cursor.fetchone()
    return {
        'gameId': game_id[0]
    }


@GAME_API.route('/setGameFinished', methods=['POST'])
def set_game_finished():
    parameters = request.get_json()
    return _set_game_finished(
        user_id=parameters['currentUser'],
        opponent=parameters['opponent']
    )


@require_token(check_user=True)
def _set_game_finished(user_id, opponent):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE game
                    SET finished = true
                    WHERE logged_in_player = %(current_user)s
                        AND other_player = %(opponent)s
                        AND finished = false
                    ''',
                    {'current_user': user_id, 'opponent': opponent}
                )
    return {}


@GAME_API.route('/fetchGameFinished/<game_id>', methods=['GET'])
def fetch_game_finished(game_id):
    return _fetch_game_finished(game_id)


@require_token()
def _fetch_game_finished(game_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT finished
                    FROM game
                    WHERE id = %(game_id)s;
                    ''',
                    {'game_id': game_id}
                )
                is_game_finished = cursor.fetchone()
    return {
        'is_game_finished': is_game_finished[0]
    }
