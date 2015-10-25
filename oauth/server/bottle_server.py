from bottle import template, Bottle, TEMPLATE_PATH
import threading
from .bottle_adapter import MyWSGIRefServer
import os


app = Bottle()
template_dir = os.path.abspath((os.path.dirname(__file__)))
TEMPLATE_PATH.insert(0, template_dir)
server = MyWSGIRefServer(host='', port=14396)


@app.get('/')
def index():
    return template('root')


def start_server():
    start_server_thread = threading.Thread(target=app.run, kwargs={'server': server, 'quiet': True})
    start_server_thread.start()


def stop_server():
    server.stop()
