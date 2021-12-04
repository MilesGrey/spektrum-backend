from flask import Blueprint, request

from db_connection import get_db_connection

from src.excerpt import get_random_excerpt_id_list
from src.authentication import require_token

USER_API = Blueprint('user_api', __name__)


@USER_API.route('/<user_id>', methods=['GET'])
def get_spektrum_user(user_id):
    return _get_spektrum_user(
        user_id=user_id
    )


@require_token(check_user=True)
def _get_spektrum_user(user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT name, profile_image_id
                    FROM spektrum_user
                    WHERE id = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                user = cursor.fetchone()
                cursor.execute(
                    '''
                    SELECT user_friend
                    FROM friend
                    WHERE logged_in_user = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                friends = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT sender
                    FROM friend_request
                    WHERE receiver = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                friend_requests = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT receiver
                    FROM friend_request
                    WHERE sender = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                pending_friend_requests = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT receiver
                    FROM game_request
                    WHERE sender = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                challenges_sent = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT sender
                    FROM game_request
                    WHERE receiver = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                challenges = cursor.fetchall()
                cursor.execute(
                    '''
                    SELECT other_player
                    FROM game
                    WHERE logged_in_player = %(user_id)s
                        AND finished = false
                    ''',
                    {'user_id': user_id}
                )
                open_games = cursor.fetchall()
    sorted_contact_list = sorted([t[0] for t in friends])
    friend_request_list = [t[0] for t in friend_requests]
    pending_friend_request_list = [t[0] for t in pending_friend_requests]

    contact_list_with_requests = []
    contact_list_with_requests.extend(friend_request_list)
    contact_list_with_requests.extend(pending_friend_request_list)
    contact_list_with_requests.extend(sorted_contact_list)
    return {
        'userId': user_id,
        'userName': user[0],
        'profileImageId': user[1],
        'contactList': contact_list_with_requests,
        'friendRequestList': friend_request_list,
        'pendingFriendRequestList': pending_friend_request_list,
        'challengeList': [t[0] for t in challenges],
        'challengeSentList': [t[0] for t in challenges_sent],
        'openGameList': [t[0] for t in open_games]
    }


@USER_API.route('/<user_id>/profileImageId', methods=['GET'])
def get_profile_image_id(user_id):
    return _get_profile_image_id(
        user_id=user_id
    )


@require_token()
def _get_profile_image_id(user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT profile_image_id
                    FROM spektrum_user
                    WHERE id = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                profile_image_id = cursor.fetchone()
    return {
        'profileImageId': profile_image_id[0]
    }


@USER_API.route('/<user_id>/userName', methods=['GET'])
def get_user_name(user_id):
    return _get_user_name(
        user_id=user_id
    )


@require_token()
def _get_user_name(user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT name
                    FROM spektrum_user
                    WHERE id = %(user_id)s
                    ''',
                    {'user_id': user_id}
                )
                user_name = cursor.fetchone()
    return {
        'userName': user_name[0]
    }


@USER_API.route('/createUser', methods=['POST'])
def create_user():
    return _create_user()


@require_token()
def _create_user():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO spektrum_user (id, name)
                    VALUES (%(user_id)s, %(user_name)s)
                    ''',
                    {'user_id': parameters['userId'], 'user_name': parameters['userName']}
                )
    return {}


@USER_API.route('/changeUserName', methods=['POST'])
def change_user_name():
    parameters = request.get_json()
    return _change_user_name(
        user_id=parameters['userId'],
        new_user_name=parameters['newUserName']
    )


@require_token(check_user=True)
def _change_user_name(user_id, new_user_name):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE spektrum_user
                    SET name = %(new_user_name)s
                    WHERE id = %(user_id)s
                    ''',
                    {'user_id': user_id, 'new_user_name': new_user_name}
                )
    return {}


@USER_API.route('/changeProfileImageId', methods=['POST'])
def change_profile_image_id():
    parameters = request.get_json()
    return _change_profile_image_id(
        user_id=parameters['userId'],
        new_profile_image_id=parameters['newProfileImageId']
    )


@require_token(check_user=True)
def _change_profile_image_id(user_id, new_profile_image_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE spektrum_user
                    SET name = %(new_profile_image_id)s
                    WHERE id = %(user_id)s
                    ''',
                    {'user_id': user_id, 'new_profile_image_id': new_profile_image_id}
                )
    return {}


@USER_API.route('/sendFriendRequest', methods=['POST'])
def send_friend_request():
    parameters = request.get_json()
    return _send_friend_request(
        user_id=parameters['userId'],
        target_user_id=parameters['targetUserId']
    )


@require_token(check_user=True)
def _send_friend_request(user_id, target_user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT EXISTS(
                      SELECT sender, receiver
                      FROM friend_request
                      WHERE sender = %(target_user_id)s
                        AND receiver = %(user_id)s
                    )
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                is_already_requested = cursor.fetchone()[0]
                if not is_already_requested:
                    cursor.execute(
                        '''
                        INSERT INTO friend_request (sender, receiver)
                        VALUES (%(user_id)s, %(target_user_id)s)
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                else:
                    cursor.execute(
                        '''
                        DELETE FROM friend_request
                        WHERE receiver = %(user_id)s
                        AND sender = %(target_user_id)s
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                    cursor.execute(
                        '''
                        INSERT INTO friend (logged_in_user, user_friend)
                        VALUES (%(user_id)s, %(target_user_id)s)
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                    cursor.execute(
                        '''
                        INSERT INTO friend (logged_in_user, user_friend)
                        VALUES (%(target_user_id)s, %(user_id)s)
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
    return {}


@USER_API.route('/acceptFriendRequest', methods=['POST'])
def accept_friend_request():
    parameters = request.get_json()
    return _accept_friend_request(
        user_id=parameters['userId'],
        target_user_id=parameters['targetUserId']
    )


@require_token(check_user=True)
def _accept_friend_request(user_id, target_user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                      DELETE FROM friend_request
                      WHERE receiver = %(user_id)s
                      AND sender = %(target_user_id)s
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                cursor.execute(
                    '''
                        INSERT INTO friend (logged_in_user, user_friend)
                        VALUES (%(user_id)s, %(target_user_id)s)
                      ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                cursor.execute(
                    '''
                        INSERT INTO friend (logged_in_user, user_friend)
                        VALUES (%(target_user_id)s, %(user_id)s)
                      ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
    return {}


@USER_API.route('/sendChallenge', methods=['POST'])
def send_challenge():
    parameters = request.get_json()
    return _send_challenge(
        user_id=parameters['userId'],
        target_user_id=parameters['targetUserId']
    )


@require_token(check_user=True)
def _send_challenge(user_id, target_user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT EXISTS(
                        SELECT sender, receiver
                        FROM game_request
                        WHERE sender = %(target_user_id)s
                            AND receiver = %(user_id)s
                    )
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                is_already_challenged = cursor.fetchone()[0]
                if not is_already_challenged:
                    cursor.execute(
                        '''
                        INSERT INTO game_request (sender, receiver)
                        VALUES (%(user_id)s, %(target_user_id)s)
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                else:
                    cursor.execute(
                        '''
                        DELETE FROM game_request
                        WHERE receiver = %(user_id)s
                        AND sender = %(target_user_id)s
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                    cursor.execute(
                        '''
                        INSERT INTO game (logged_in_player, other_player)
                        VALUES (%(user_id)s, %(target_user_id)s)
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                    cursor.execute(
                        '''
                        INSERT INTO game (game_created, logged_in_player, other_player)
                        VALUES (
                            (
                            SELECT game_created
                            FROM game
                            WHERE logged_in_player = %(user_id)s
                                AND other_player = %(target_user_id)s
                                AND finished = false
                            ), %(target_user_id)s, %(user_id)s
                        )
                        ''',
                        {'user_id': user_id, 'target_user_id': target_user_id}
                    )
                    cursor.execute(
                        '''
                        SELECT id
                        FROM game
                        WHERE (
                          (
                            logged_in_player = %(logged_in_player)s
                            AND other_player = %(other_player)s
                          ) OR (
                            logged_in_player = %(other_player)s
                            AND other_player = %(logged_in_player)s
                          )
                        )
                        AND finished = false
                        ''',
                        {'logged_in_player': user_id, 'other_player': target_user_id}
                    )
                    game_map = cursor.fetchall()
                    excerpt_id_list = get_random_excerpt_id_list()
                    for i, excerpt in enumerate(excerpt_id_list):
                        for row in game_map:
                            cursor.execute(
                                '''
                                INSERT INTO game_excerpt (game_id, counter, speech_id, fragment)
                                VALUES (%(game_id)s, %(counter)s, %(speech_id)s, %(fragment)s)
                                ''',
                                {
                                    'game_id': row[0],
                                    'counter': i,
                                    'speech_id': excerpt['speechId'],
                                    'fragment': excerpt['fragment'],
                                }
                            )
    return {}


@USER_API.route('/acceptChallenge', methods=['POST'])
def accept_challenge():
    parameters = request.get_json()
    return _accept_challenge(
        user_id=parameters['userId'],
        target_user_id=parameters['targetUserId']
    )


@require_token(check_user=True)
def _accept_challenge(user_id, target_user_id):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    DELETE FROM game_request
                    WHERE receiver = %(user_id)s
                    AND sender = %(target_user_id)s
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                cursor.execute(
                    '''
                    INSERT INTO game (logged_in_player, other_player)
                    VALUES (%(user_id)s, %(target_user_id)s)
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                cursor.execute(
                    '''
                    INSERT INTO game (game_created, logged_in_player, other_player)
                    VALUES (
                        (
                        SELECT game_created
                        FROM game
                        WHERE logged_in_player = %(user_id)s
                            AND other_player = %(target_user_id)s
                            AND finished = false
                        ), %(target_user_id)s, %(user_id)s
                    )
                    ''',
                    {'user_id': user_id, 'target_user_id': target_user_id}
                )
                cursor.execute(
                    '''
                    SELECT id
                    FROM game
                    WHERE (
                      (
                        logged_in_player = %(logged_in_player)s
                        AND other_player = %(other_player)s
                      ) OR (
                        logged_in_player = %(other_player)s
                        AND other_player = %(logged_in_player)s
                      )
                    )
                    AND finished = false
                    ''',
                    {'logged_in_player': user_id, 'other_player': target_user_id}
                )
                game_map = cursor.fetchall()
                excerpt_id_list = get_random_excerpt_id_list()
                for i, excerpt in enumerate(excerpt_id_list):
                    for row in game_map:
                        cursor.execute(
                            '''
                            INSERT INTO game_excerpt (game_id, counter, speech_id, fragment)
                            VALUES (%(game_id)s, %(counter)s, %(speech_id)s, %(fragment)s)
                            ''',
                            {
                                'game_id': row[0],
                                'counter': i,
                                'speech_id': excerpt['speechId'],
                                'fragment': excerpt['fragment'],
                            }
                        )
    return {}
