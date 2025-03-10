from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from app import app, socketio

if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app, handler_class=WebSocketHandler)
    http_server.serve_forever()