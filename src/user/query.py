from src.excerpt.query import get_random_excerpt_id_list


def get_spektrum_user(user_id, cursor):
    cursor.execute(
        '''
        SELECT name, profile_image_id
        FROM spektrum_user
        WHERE id = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    user = cursor.fetchone()
    return {
        'userId': user_id,
        'userName': user[0],
        'profileImageId': user[1]
    }


def get_friends(user_id, cursor):
    cursor.execute(
        '''
        SELECT user_friend
        FROM friend
        WHERE logged_in_user = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    friends = cursor.fetchall()
    return sorted([t[0] for t in friends])


def get_friend_requests(user_id, cursor):
    cursor.execute(
        '''
        SELECT sender
        FROM friend_request
        WHERE receiver = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    friend_requests = cursor.fetchall()
    return [t[0] for t in friend_requests]


def get_pending_friend_requests(user_id, cursor):
    cursor.execute(
        '''
        SELECT receiver
        FROM friend_request
        WHERE sender = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    pending_friend_requests = cursor.fetchall()
    return [t[0] for t in pending_friend_requests]


def get_challenges_sent(user_id, cursor):
    cursor.execute(
        '''
        SELECT receiver
        FROM game_request
        WHERE sender = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    challenges_sent = cursor.fetchall()
    return [t[0] for t in challenges_sent]


def get_challenges(user_id, cursor):
    cursor.execute(
        '''
        SELECT sender
        FROM game_request
        WHERE receiver = %(user_id)s
        ''',
        {'user_id': user_id}
    )
    challenges = cursor.fetchall()
    return [t[0] for t in challenges]


def get_open_games(user_id, cursor):
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
    return [t[0] for t in open_games]


def create_user(user_id, user_name, cursor):
    cursor.execute(
        '''
        INSERT INTO spektrum_user (id, name)
        VALUES (%(user_id)s, %(user_name)s)
        ''',
        {'user_id': user_id, 'user_name': user_name}
    )
    return {}


def change_user_name(user_id, new_user_name, cursor):
    cursor.execute(
        '''
        UPDATE spektrum_user
        SET name = %(new_user_name)s
        WHERE id = %(user_id)s
        ''',
        {'user_id': user_id, 'new_user_name': new_user_name}
    )
    return {}


def change_profile_image_id(user_id, new_profile_image_id, cursor):
    cursor.execute(
        '''
        UPDATE spektrum_user
        SET name = %(new_profile_image_id)s
        WHERE id = %(user_id)s
        ''',
        {'user_id': user_id, 'new_profile_image_id': new_profile_image_id}
    )
    return {}


def send_friend_request(user_id, target_user_id, cursor):
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


def accept_friend_request(user_id, target_user_id, cursor):
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


def send_challenge(user_id, target_user_id, cursor):
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


def accept_challenge(user_id, target_user_id, cursor):
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
