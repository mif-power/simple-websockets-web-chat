# Simple WebSocket Web Chat

A lightweight, real-time group chat application built with Flask and Socket.IO. Features username persistence via localStorage, real-time messaging, and a clean responsive interface.

## Features

- ✅ Real-time messaging via WebSocket (Socket.IO)
- ✅ Username persistence using browser localStorage
- ✅ Mandatory username before sending messages
- ✅ Message history displayed on connection
- ✅ Responsive design (works on mobile and desktop)
- ✅ Lightweight and easy to deploy
- ✅ Docker support with restart policy

## Access the Application

Once deployed, the chat is available at:
```
http://<your-server-ip>:5000
```

## Local Development / Manual Start

### Prerequisites
- Python 3.7+
- pip

### Setup
```bash
# Clone or copy the project
git clone https://github.com/mif-power/simple-websockets-web-chat.git
# or copy the python_chat directory

cd python_chat

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start the Server
```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Start the chat server
python app.py
```

The server will start on http://0.0.0.0:5000 (accessible via your server's IP).

### Run in Background (Production)
```bash
nohup python app.py > chat.log 2>&1 &
```

### Stop the Server
```bash
pkill -f "python.*app.py" || pkill -f "flask" || true
```

### View Logs
```bash
tail -f chat.log
```

## Docker Deployment

### Build the Image
```bash
docker build -t web-chat .
```

### Run the Container
```bash
docker run -d \
  --name web-chat \
  -p 5000:5000 \
  --restart unless-stopped \
  web-chat
```

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

This will:
- Build the image (if needed)
- Start the container
- Apply restart policy (unless-stopped)
- Expose port 5000 on the host

### Manage with Docker Compose
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart
```

## How It Works

### Username Persistence
- On first visit, users are prompted to enter a name
- The name is saved to `localStorage` under `chatUserName`
- On subsequent visits, the name is automatically retrieved
- Users cannot send messages without providing a name
- Name can be changed by clearing browser storage or accessing incognito/private mode

### Real-Time Communication
- Uses Socket.IO for bidirectional WebSocket communication
- Server broadcasts messages to all connected clients
- Message history is sent to new connections
- All messages include the sender's username

## File Structure
```
.
├── app.py                 # Main Flask-SocketIO application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker build instructions
├── docker-compose.yml     # Docker-Compose configuration
├── README.md              # This file
├── templates/
│   └── index.html         # Main chat interface
└── chat.log               # Runtime log (when started with nohup)
```

## Customization

### Change Port
Edit `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

### Disable Debug Mode (Production)
In `app.py`, set `debug=False`:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

### Add Authentication
Currently uses anonymous username system. To add proper authentication:
1. Modify the join logic in `index.html`
2. Add user validation in Socket.IO handlers
3. Consider integrating with Flask-Login or similar

## Dependencies
- Flask==3.1.3
- Flask-SocketIO==5.6.1
- eventlet==0.41.0
- python-socketio==5.16.1
- python-engineio==4.13.1

## License
MIT License - feel free to modify and use as needed.

## Support
For issues or questions, please open an issue on the GitHub repository:
https://github.com/mif-power/simple-websockets-web-chat/issues

---
*Built with ❤️ using Flask and Socket.IO*
