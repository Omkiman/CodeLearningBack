from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from models import db
from api import api, set_rooms_reference
from sockets import init_socket_handlers
from db_init import init_database

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codeblocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   ping_timeout=20, 
                   ping_interval=10, 
                   async_mode=None) 
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
