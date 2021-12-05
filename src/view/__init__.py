from flask import Blueprint, request

from src.authentication import require_token
from src.db_connection import get_db_connection
from src.excerpt.query import get_excerpt_list_for_game
from src.game.query import get_game, get_player
from src.result.query import fetch_results_by_game_id, get_current_total_distance
from src.speaker.query import fetch_all_speaker_ids
from src.user.query import get_spektrum_user, get_friends, get_friend_requests, get_pending_friend_requests, \
    get_challenges_sent, get_challenges, get_open_games

VIEW_API = Blueprint('views_api', __name__)


@VIEW_API.route('/contactPage', methods=['POST'])
def get_contact_page():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_contact_page(
                    cursor=cursor,
                    user_id=parameters['userId']
                )


@require_token(check_user=True)
def _get_contact_page(cursor, user_id):
    user = get_spektrum_user(user_id, cursor)
    friends = get_friends(user_id, cursor)
    friend_requests = get_friend_requests(user_id, cursor)
    pending_friend_requests = get_pending_friend_requests(user_id, cursor)
    challenges_sent = get_challenges_sent(user_id, cursor)
    challenges = get_challenges(user_id, cursor)
    open_games = get_open_games(user_id, cursor)
    speaker_id_list = fetch_all_speaker_ids(cursor)
    contact_list_with_requests = []
    contact_list_with_requests.extend(friend_requests)
    contact_list_with_requests.extend(pending_friend_requests)
    contact_list_with_requests.extend(friends)
    return {
        'user': user,
        'contactList': contact_list_with_requests,
        'friendRequestList': friend_requests,
        'pendingFriendRequestList': pending_friend_requests,
        'challengeList': challenges,
        'challengeSentList': challenges_sent,
        'openGameList': open_games,
        'speakerIdList': speaker_id_list
    }


@VIEW_API.route('/preGamePage', methods=['POST'])
def get_pre_game_page():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_pre_game_page(
                    user_id=parameters['userId'],
                    opponent_id=parameters['opponentId'],
                    cursor=cursor
                )


@require_token(check_user=True)
def _get_pre_game_page(cursor, user_id, opponent_id):
    opponent = get_spektrum_user(opponent_id, cursor)

    user_game = get_game(user_id, opponent_id, cursor)
    opponent_game = get_game(opponent_id, user_id, cursor)

    user_total_distance = get_current_total_distance(user_game['gameId'], cursor)
    opponent_total_distance = get_current_total_distance(opponent_game['gameId'], cursor)

    user_game_info = {
        'gameId': user_game['gameId'],
        'isFinished': user_game['isFinished'],
        'totalDistance': user_total_distance
    }
    opponent_game_info = {
        'gameId': opponent_game['gameId'],
        'isFinished': opponent_game['isFinished'],
        'totalDistance': opponent_total_distance
    }

    return {
        'opponent': opponent,
        'userGame': user_game_info,
        'opponentGame': opponent_game_info
    }


@VIEW_API.route('/gamePage', methods=['POST'])
def get_game_page():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = get_player(parameters['gameId'], cursor)
                return _get_game_page(
                    user_id=user_id,
                    game_id=parameters['gameId'],
                    cursor=cursor
                )


@require_token(check_user=True)
def _get_game_page(cursor, user_id, game_id):
    excerpt_list = get_excerpt_list_for_game(game_id, cursor)
    result_list = fetch_results_by_game_id(game_id, cursor)
    return {
        'gameId': game_id,
        'excerptList': excerpt_list,
        'resultList': result_list
    }
