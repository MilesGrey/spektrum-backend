def fetch_all_speaker_ids(cursor):
    cursor.execute(
        '''
        SELECT DISTINCT id
        FROM speaker
        '''
    )
    result_list = cursor.fetchall()
    return [speaker[0] for speaker in result_list]
