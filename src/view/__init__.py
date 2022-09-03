from flask import request

from __main__ import socketio, session_to_user

from src.db_connection import get_db_connection
from src.excerpt.query import get_excerpt_list_for_game
from src.game.query import get_latest_game, get_players, get_game, get_game_by_creation
from src.result.query import fetch_results_by_game_id, get_game_info
from src.speaker.query import fetch_all_speaker_ids_with_image
from src.user.query import get_spektrum_user, get_friends, get_friend_requests, get_pending_friend_requests, \
    get_challenges_sent, get_challenges, get_open_games, get_finished_games


@socketio.on('view_contact_page')
def get_contact_page(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_contact_page(
                    cursor=cursor,
                    user_id=json['userId'],
                )


@socketio.on('view_pre_game_page')
def get_pre_game_page(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id = session_to_user[request.sid]
                return _get_pre_game_page(
                    user_id=user_id,
                    opponent_id=json['opponentId'],
                    cursor=cursor
                )


@socketio.on('view_history_game_page')
def get_history_game_page(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_history_game_page(
                    game_id=json['gameId'],
                    cursor=cursor
                )


@socketio.on('view_game_page')
def get_game_page(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                user_id, _ = get_players(json['gameId'], cursor)
                if user_id != session_to_user[request.sid]:
                    return 'no-such-game'
                return _get_game_page(
                    game_id=json['gameId'],
                    cursor=cursor
                )


def _get_contact_page(cursor, user_id):
    user = get_spektrum_user(user_id, cursor)
    friends = get_friends(user_id, cursor)
    friend_requests = get_friend_requests(user_id, cursor)
    pending_friend_requests = get_pending_friend_requests(user_id, cursor)
    challenges_sent = get_challenges_sent(user_id, cursor)
    challenges = get_challenges(user_id, cursor)
    open_games = get_open_games(user_id, cursor)
    finished_games = get_finished_games(user_id, cursor)
    speaker_id_list = fetch_all_speaker_ids_with_image(cursor)
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
        'speakerIdList': speaker_id_list,
        'finishedGameList': finished_games
    }


def _get_pre_game_page(cursor, user_id, opponent_id):
    opponent = get_spektrum_user(opponent_id, cursor)

    user_game = get_latest_game(user_id, opponent_id, cursor)
    opponent_game = get_latest_game(opponent_id, user_id, cursor)

    user_game_info = get_game_info(user_game, cursor)
    opponent_game_info = get_game_info(opponent_game, cursor)

    return {
        'opponent': opponent,
        'userGame': user_game_info,
        'opponentGame': opponent_game_info
    }


def _get_history_game_page(cursor, game_id):
    user_game = get_game(game_id, cursor)
    opponent = get_spektrum_user(user_game['otherPlayer'], cursor)
    opponent_game = get_game_by_creation(
        logged_in_player=user_game['otherPlayer'],
        other_player=user_game['loggedInPlayer'],
        game_created=user_game['gameCreated'],
        cursor=cursor
    )
    user_game_info = get_game_info(user_game, cursor)
    opponent_game_info = get_game_info(opponent_game, cursor)

    return {
        'opponent': opponent,
        'userGame': user_game_info,
        'opponentGame': opponent_game_info
    }


def _get_game_page(cursor, game_id):
    excerpt_list = get_excerpt_list_for_game(game_id, cursor)
    result_list = fetch_results_by_game_id(game_id, cursor)
    return {
        'gameId': game_id,
        'excerptList': excerpt_list,
        'resultList': result_list
    }
