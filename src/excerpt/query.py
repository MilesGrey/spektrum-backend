from src.db_connection import get_db_connection


def get_random_excerpt_id_list():
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT speech_id, fragment
                    FROM excerpt
                    WHERE report_count < 3
                    ORDER BY RANDOM()
                    LIMIT 3;
                    '''
                )
                excerpt_list = cursor.fetchall()
    return [{'speechId': excerpt[0], 'fragment': excerpt[1]} for excerpt in excerpt_list]


def get_excerpt_list_for_game(game_id, cursor):
    cursor.execute(
        '''
        SELECT DISTINCT excerpt_information.id, excerpt_information.first_name,
            excerpt_information.last_name, excerpt_information.party,
            excerpt_information.socio_cultural_coordinate, excerpt_information.socio_economic_coordinate,
            excerpt_information.excerpt, excerpt_information.speech_id, excerpt_information.fragment,
            excerpt_information.topic, game_excerpt.counter, excerpt_information.bio
        FROM (
            SELECT speaker_party.id, speaker_party.first_name, speaker_party.last_name, speaker_party.party,
                speaker_party.bio, speaker_party.socio_cultural_coordinate,
                speaker_party.socio_economic_coordinate, excerpt_speech.excerpt, excerpt_speech.speech_id,
                excerpt_speech.fragment, excerpt_speech.topic
            FROM (
                SELECT excerpt.excerpt, speech.speaker_id, excerpt.speech_id, excerpt.fragment,
                    excerpt.topic
                FROM excerpt
                INNER JOIN speech
                    ON excerpt.speech_id = speech.id
            ) AS excerpt_speech
            INNER JOIN (
                SELECT speaker.id, speaker.first_name, speaker.last_name, speaker.party,
                    speaker.bio, party.socio_cultural_coordinate, party.socio_economic_coordinate
                FROM speaker
                INNER JOIN party
                    ON speaker.party = party.name
            ) AS speaker_party
                ON excerpt_speech.speaker_id = speaker_party.id
        ) AS excerpt_information
        INNER JOIN game_excerpt
            ON excerpt_information.speech_id = game_excerpt.speech_id
                AND excerpt_information.fragment = game_excerpt.fragment
        WHERE game_excerpt.speech_id IN (
            SELECT speech_id
            FROM game_excerpt
            WHERE game_id = %(game_id)s
        )
            AND game_excerpt.fragment IN (
                SELECT fragment
                FROM game_excerpt
                WHERE game_id = %(game_id)s
            )
        ''',
        {'game_id': game_id}
    )
    result_list = cursor.fetchall()
    excerpt_list = [
        {
            'speakerId': excerpt[0],
            'speakerFirstName': excerpt[1],
            'speakerLastName': excerpt[2],
            'party': excerpt[3],
            'socioCulturalCoordinate': excerpt[4],
            'socioEconomicCoordinate': excerpt[5],
            'content': excerpt[6],
            'speechId': excerpt[7],
            'fragment': excerpt[8],
            'topic': excerpt[9],
            'counter': excerpt[10],
            'bio': excerpt[11],
        }
        for excerpt in result_list
    ]
    return sorted(excerpt_list, key=lambda excerpt: excerpt['counter'])


def report(speech_id, fragment):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE excerpt
                    SET report_count = report_count + 1
                    WHERE speech_id = %(speech_id)s AND fragment = %(fragment)s
                    ''',
                    {'speech_id': speech_id, 'fragment': fragment}
                )
    return {}
