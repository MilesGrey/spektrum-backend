from firebase_admin import messaging


def send_notification_to_token(registration_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=registration_token,
    )
    messaging.send(message)
