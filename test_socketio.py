import socketio
from socketio.exceptions import TimeoutError

sio = socketio.Client(logger=True, engineio_logger=True)
previous_conversations = ""
@sio.event(namespace='/chat')
def connect():
    print('connected to server')
    sio.emit(event='joined',data={'room':'1'}, namespace='/chat')


@sio.on('history', namespace='/chat')
def history(data):
    global previous_conversations
    print('receiving historical message')
    message_sender, message_content = data['msg'].split(sep=(':'))
    previous_conversations+= message_content+' '
    sio.emit(event='message',data={'room':"1", 'bot':True, 'msg':'Hello, Biar saya proses dulu informasi kamu ya'}, namespace='/chat')

@sio.event(namespace='/chat')
def message(data):
    try:
        message_sender, message_content = data['msg'].split(sep=(':'))
        print(message_sender)
        if message_sender.lower() !='bot':
            print(f'{message_sender}: {message_content}')
            sio.emit(event='message',data={'room':"1", 'bot':True, 'msg':'Reply from bot'}, namespace='/chat')
        else:
            pass
    except:
        pass

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:5000', namespaces=['/chat'])
sio.wait()