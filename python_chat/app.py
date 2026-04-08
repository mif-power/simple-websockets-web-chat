from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Хранение сообщений в памяти (для простоты)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # data: { 'msg': str, 'user': str }
    messages.append(data)
    emit('message', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Отправляем историю сообщений новому пользователю
    emit('history', messages)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
