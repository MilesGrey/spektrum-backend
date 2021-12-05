from flask import Blueprint

from src.authentication import require_token
from src.db_connection import get_db_connection
from src.game import query
from src.game.query import get_player

GAME_API = Blueprint('game_api', __name__)


@GAME_API.route('/setGameFinished/<game_id>', methods=['GET'])
def set_game_finished(game_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = get_player(game_id, cursor)
                return _set_game_finished(
                    cursor=cursor,
                    user_id=user_id,
                    game_id=game_id
                )


@require_token(check_user=True)
def _set_game_finished(cursor, user_id, game_id):
    return query.set_game_finished(
        game_id=game_id,
        cursor=cursor
    )
