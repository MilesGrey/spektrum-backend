def get_latest_game(user_id, other_player, cursor):
    cursor.execute(
        '''
        SELECT id, finished
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
    game = cursor.fetchone()
    return {
        'gameId': game[0],
        'isFinished': game[1]
    }


def get_game(game_id, cursor):
    cursor.execute(
        '''
        SELECT id, game_created, logged_in_player, other_player, finished
        FROM game
        WHERE id = %(game_id)s
        ''',
        {'game_id': game_id}
    )
    game = cursor.fetchone()
    return {
        'gameId': game[0],
        'gameCreated': game[1],
        'loggedInPlayer': game[2],
        'otherPlayer': game[3],
        'isFinished': game[4]
    }


def get_game_by_creation(logged_in_player, other_player, game_created, cursor):
    cursor.execute(
        '''
        SELECT id, game_created, logged_in_player, other_player, finished
        FROM game
        WHERE logged_in_player = %(logged_in_player)s
            AND other_player = %(other_player)s
            AND game_created = %(game_created)s
        ''',
        {'logged_in_player': logged_in_player, 'other_player': other_player, 'game_created': game_created}
    )
    game = cursor.fetchone()
    return {
        'gameId': game[0],
        'gameCreated': game[1],
        'loggedInPlayer': game[2],
        'otherPlayer': game[3],
        'isFinished': game[4]
    }


def get_players(game_id, cursor):
    cursor.execute(
        '''
        SELECT logged_in_player, other_player
        FROM game
        WHERE id = %(game_id)s
        ''',
        {'game_id': game_id}
    )
    game = cursor.fetchone()
    return game[0], game[1]


def set_game_finished(game_id, cursor):
    cursor.execute(
        '''
        UPDATE game
        SET finished = true
        WHERE id = %(game_id)s
        ''',
        {'game_id': game_id}
    )
    return {}
