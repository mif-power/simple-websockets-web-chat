from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.user}: {self.msg[:20]}>'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # data: { 'msg': str, 'user': str }
    msg_entry = Message(user=data['user'], msg=data['msg'])
    db.session.add(msg_entry)
    db.session.commit()
    # Emit with timestamp formatted
    timestamp_str = msg_entry.timestamp.strftime("%H:%M")
    emit('message', {
        'msg': msg_entry.msg,
        'user': msg_entry.user,
        'timestamp': timestamp_str
    }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Send last 100 messages as history
    recent = Message.query.order_by(Message.timestamp.desc()).limit(100).all()
    # Reverse to chronological order
    recent = list(reversed(recent))
    history = []
    for m in recent:
        history.append({
            'msg': m.msg,
            'user': m.user,
            'timestamp': m.timestamp.strftime("%H:%M")
        })
    emit('history', history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
