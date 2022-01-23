from flask_socketio import emit

from __main__ import socketio, user_to_session

from src.push_notifications import send_notification_to_token
from src.db_connection import get_db_connection
from src.user import query


@socketio.on('register_notification_token')
def register_notification_token(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _register_notification_token(
                    cursor=cursor,
                    user_id=json['userId'],
                    notification_token=json['notificationToken']
                )


@socketio.on('get_spektrum_user')
def get_spektrum_user(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _get_spektrum_user(
                    cursor=cursor,
                    user_id=json['userId'],
                )


@socketio.on('user_create_user')
def create_user(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _create_user(
                    cursor=cursor,
                    user_id=json['userId'],
                    user_name=json['userName']
                )


@socketio.on('user_change_user_name')
def change_user_name(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _change_user_name(
                    cursor=cursor,
                    user_id=json['userId'],
                    new_user_name=json['newUserName']
                )


@socketio.on('user_change_profile_image_id')
def change_profile_image_id(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _change_profile_image_id(
                    user_id=json['userId'],
                    new_profile_image_id=json['newProfileImageId'],
                    cursor=cursor
                )


@socketio.on('user_send_friend_request')
def send_friend_request(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                response = _send_friend_request(
                    cursor=cursor,
                    user_id=json['userId'],
                    target_user_id=json['targetUserId']
                )
                target_notification_token = query.get_notification_token(
                    user_id=json['targetUserId'],
                    cursor=cursor
                )
    try:
        target_user_sid = user_to_session[json['targetUserId']]
        emit('new_friend_request', {'userId': json['userId']}, broadcast=True, to=target_user_sid)
    except KeyError:
        pass
    send_notification_to_token(
        registration_token=target_notification_token,
        title='neue freundschaftsanfrage',
        body=f'{json["userId"]} hat dir eine freundschaftsanfrage geschickt.'
    )
    return response


@socketio.on('user_accept_friend_request')
def accept_friend_request(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                response = _accept_friend_request(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
                    cursor=cursor
                )
    try:
        target_user_sid = user_to_session[json['targetUserId']]
        emit('friend_request_accepted', {'userId': json['userId']}, broadcast=True, to=target_user_sid)
    except KeyError:
        pass
    return response


@socketio.on('user_send_challenge')
def send_challenge(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                response = _send_challenge(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
                    cursor=cursor
                )
                target_notification_token = query.get_notification_token(
                    user_id=json['targetUserId'],
                    cursor=cursor
                )
    try:
        target_user_sid = user_to_session[json['targetUserId']]
        emit('new_challenge', {'userId': json['userId']}, broadcast=True, to=target_user_sid)
    except KeyError:
        pass
    send_notification_to_token(
        registration_token=target_notification_token,
        title='neue herausforderung',
        body=f'{json["userId"]} hat dich zu einem spiel herausgefordert.'
    )
    return response


@socketio.on('user_accept_challenge')
def accept_challenge(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                response = _accept_challenge(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
                    cursor=cursor
                )
    try:
        target_user_sid = user_to_session[json['targetUserId']]
        emit('challenge_accepted', {'userId': json['userId']}, broadcast=True, to=target_user_sid)
    except KeyError:
        pass
    return response


def _register_notification_token(cursor, user_id, notification_token):
    return query.register_notification_token(
        user_id=user_id,
        notification_token=notification_token,
        cursor=cursor
    )


def _get_spektrum_user(cursor, user_id):
    return query.get_spektrum_user(
        user_id=user_id,
        cursor=cursor
    )


def _create_user(cursor, user_id, user_name):
    return query.create_user(
        user_id=user_id,
        user_name=user_name,
        cursor=cursor
    )


def _change_user_name(cursor, user_id, new_user_name):
    return query.change_user_name(
        user_id=user_id,
        new_user_name=new_user_name,
        cursor=cursor
    )


def _change_profile_image_id(cursor, user_id, new_profile_image_id):
    return query.change_profile_image_id(
        user_id=user_id,
        new_profile_image_id=new_profile_image_id,
        cursor=cursor
    )


def _send_friend_request(cursor, user_id, target_user_id):
    return query.send_friend_request(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


def _accept_friend_request(cursor, user_id, target_user_id):
    return query.accept_friend_request(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


def _send_challenge(cursor, user_id, target_user_id):
    return query.send_challenge(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


def _accept_challenge(cursor, user_id, target_user_id):
    return query.accept_challenge(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )
