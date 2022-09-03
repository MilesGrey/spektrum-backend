from __main__ import socketio

from src.db_connection import get_db_connection
from src.image.query import get_copyright


IMAGES_DIRECTORY = 'portrait_id'


@socketio.on('image_politician')
def get_politician_image(json):
    return _get_politician_image(
        speaker_id=json['speakerId'],
    )


def _get_politician_image(speaker_id):
    image_data = None
    if speaker_id.isdigit():
        with open(f'{IMAGES_DIRECTORY}/{speaker_id}.jpg', 'rb') as f:
            image_data = f.read()
    return image_data


@socketio.on('image_copyright')
def get_copyright_image(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_copyright_image(
                    cursor=cursor,
                    speaker_id=json['speakerId'],
                )


def _get_copyright_image(cursor, speaker_id):
    return get_copyright(speaker_id, cursor)