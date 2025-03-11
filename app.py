from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from models import db
from api import api, set_rooms_reference
from sockets import init_socket_handlers
from db_init import init_database
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": ["https://tomswatchingfromthailand.netlify.app"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codeblocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    ping_timeout=30,
    ping_interval=15,
    async_mode='gevent',
    transports=['websocket']
)

rooms = {}

# Register the API blueprint
app.register_blueprint(api)

# Share the rooms reference with the API module
set_rooms_reference(rooms)

# Initialize Socket.IO handlers
init_socket_handlers(socketio, rooms)

# Initialize the database
init_database(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)
