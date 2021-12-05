from flask import Blueprint, request

from src.authentication import require_token
from src.db_connection import get_db_connection
from src.user import query

USER_API = Blueprint('user_api', __name__)


@USER_API.route('/createUser', methods=['POST'])
def create_user():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _create_user(
                    cursor=cursor,
                    user_id=parameters['userId'],
                    user_name=parameters['user_name']
                )


@require_token(check_user=True)
def _create_user(cursor, user_id, user_name):
    return query.create_user(
        user_id=user_id,
        user_name=user_name,
        cursor=cursor
    )


@USER_API.route('/changeUserName', methods=['POST'])
@require_token()
def change_user_name():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _change_user_name(
                    cursor=cursor,
                    user_id=parameters['userId'],
                    new_user_name=parameters['newUserName']
                )


@require_token(check_user=True)
def _change_user_name(cursor, user_id, new_user_name):
    return query.change_user_name(
        user_id=user_id,
        new_user_name=new_user_name,
        cursor=cursor
    )


@USER_API.route('/changeProfileImageId', methods=['POST'])
@require_token()
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


@require_token(check_user=True)
def _change_profile_image_id(cursor, user_id, new_profile_image_id):
    return query.change_profile_image_id(
        user_id=user_id,
        new_profile_image_id=new_profile_image_id,
        cursor=cursor
    )


@USER_API.route('/sendFriendRequest', methods=['POST'])
def send_friend_request():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _send_friend_request(
                    cursor=cursor,
                    user_id=parameters['userId'],
                    target_user_id=parameters['targetUserId']
                )


@require_token(check_user=True)
def _send_friend_request(cursor, user_id, target_user_id):
    return query.send_friend_request(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


@USER_API.route('/acceptFriendRequest', methods=['POST'])
def accept_friend_request():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _accept_friend_request(
                    user_id=parameters['userId'],
                    target_user_id=parameters['targetUserId'],
                    cursor=cursor
                )


@require_token(check_user=True)
def _accept_friend_request(cursor, user_id, target_user_id):
    return query.accept_friend_request(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


@USER_API.route('/sendChallenge', methods=['POST'])
@require_token()
def send_challenge():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _send_challenge(
                    user_id=parameters['userId'],
                    target_user_id=parameters['targetUserId'],
                    cursor=cursor
                )


def _send_challenge(cursor, user_id, target_user_id):
    return query.send_challenge(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )


@USER_API.route('/acceptChallenge', methods=['POST'])
@require_token()
def accept_challenge():
    parameters = request.get_json()
    with get_db_connection() as connection:
        with connection:
            with connection.cursor() as cursor:
                return _accept_challenge(
                    user_id=parameters['userId'],
                    target_user_id=parameters['targetUserId'],
                    cursor=cursor
                )


def _accept_challenge(cursor, user_id, target_user_id):
    return query.accept_challenge(
        user_id=user_id,
        target_user_id=target_user_id,
        cursor=cursor
    )
