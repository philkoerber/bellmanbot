import eventlet
eventlet.monkey_patch()
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from celery_config import make_celery
from blueprints import train_bp, predict_bp, download_bp, instrument_info_bp

app = Flask(__name__)
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, message_queue='redis://redis:6379/0', cors_allowed_origins="*")

celery = make_celery(app)

# Register the blueprints
app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')
app.register_blueprint(instrument_info_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Bellmanbot Flask server!"})

@socketio.on('connect')
def handshake_for_verifying_connection():
    socketio.emit('hello_handshake', {'message': "Socket handshake from server"})

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
