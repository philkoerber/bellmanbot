from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from celery_config import make_celery
from blueprints import train_bp, predict_bp, download_bp

app = Flask(__name__)
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

celery = make_celery(app)

app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Bellmanbot Flask server!"})

# Sample SocketIO event
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():  # Keep this for disconnection
    print('Client disconnected')

@socketio.on('test_button')
def handle_test_button():
    print('Test Button clicked')
    socketio.emit('test_button_response', {'data': 'Button was clickeddd!'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
