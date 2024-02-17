from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from collections import namedtuple
import redis

redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)
history = {}

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    for items in list(redis_server.smembers(f"room:{room}")):
        emit('message', {'msg': items.split(sep=":")[0] + ':' + items.split(sep=":")[1]}, room=room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    redis_server.sadd(f"room:{room}",f"{session.get('name')}:{message['msg']}")
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

