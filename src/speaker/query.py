def fetch_all_speaker_ids_with_image(cursor):
    cursor.execute(
        '''
        SELECT DISTINCT id
        FROM speaker
        WHERE copyright IS NOT NULL;
        '''
    )
    result_list = cursor.fetchall()
    return [speaker[0] for speaker in result_list]
