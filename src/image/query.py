def get_copyright(speaker_id, cursor):
    cursor.execute(
        '''
        SELECT copyright
        FROM speaker
        WHERE id = %(speaker_id)s
        ''',
        {'speaker_id': speaker_id}
    )
    game = cursor.fetchone()
    return {
        'copyright': game[0],
    }