from __main__ import socketio

from src.excerpt import query


@socketio.on('excerpt_report')
def report(json):
    return query.report(
        speech_id=json['speechId'],
        fragment=json['fragment']
    )
