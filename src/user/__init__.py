from flask import request

from __main__ import socketio

from src.db_connection import get_db_connection
from src.user import query


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
def change_profile_image_id():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _change_profile_image_id(
                    user_id=parameters['userId'],
                    new_profile_image_id=parameters['newProfileImageId'],
                    cursor=cursor
                )


@socketio.on('user_send_friend_request')
def send_friend_request(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _send_friend_request(
                    cursor=cursor,
                    user_id=json['userId'],
                    target_user_id=json['targetUserId']
                )


@socketio.on('user_accept_friend_request')
def accept_friend_request(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _accept_friend_request(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
                    cursor=cursor
                )


@socketio.on('user_send_challenge')
def send_challenge(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _send_challenge(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
                    cursor=cursor
                )


@socketio.on('user_accept_challenge')
def accept_challenge(json):
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _accept_challenge(
                    user_id=json['userId'],
                    target_user_id=json['targetUserId'],
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
