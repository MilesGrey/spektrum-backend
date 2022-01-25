def fetch_results_by_game_id(game_id, cursor):
    cursor.execute(
        '''
        SELECT game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate,
            distance
        FROM result
        WHERE game_id = %(game_id)s
        ''',
        {'game_id': game_id}
    )
    result_list = cursor.fetchall()
    return [
        {
            'gameId': result[0],
            'excerptCounter': result[1],
            'userId': result[2],
            'socioCulturalCoordinate': result[3],
            'socioEconomicCoordinate': result[4],
            'distance': result[5]
        }
        for result in result_list
    ]


def get_game_info(game, cursor):
    cursor.execute(
        '''
        SELECT distance
        FROM result
        WHERE game_id = %(game_id)s
        ''',
        {'game_id': game['gameId']}
    )
    distances = cursor.fetchall()
    return {
        'gameId': game['gameId'],
        'isFinished': game['gameId'],
        'totalDistance': float(sum([distance[0] for distance in distances]))
    }


def store(game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate, distance, cursor):
    cursor.execute(
        '''
        INSERT INTO result (
            game_id, excerpt_counter, user_id, socio_cultural_coordinate, socio_economic_coordinate,
            distance
        )
        VALUES (
            %(game_id)s, %(excerpt_counter)s, %(user_id)s, %(socio_cultural_coordinate)s,
            %(socioEconomicCoordinate)s, %(distance)s
        )
        ''',
        {
            'game_id': game_id,
            'excerpt_counter': excerpt_counter,
            'user_id': user_id,
            'socio_cultural_coordinate': socio_cultural_coordinate,
            'socioEconomicCoordinate': socio_economic_coordinate,
            'distance': distance
        }
    )
    return {}
