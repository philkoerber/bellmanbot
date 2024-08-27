from flask import Flask, jsonify
from flask_cors import CORS
from celery_config import make_celery

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure Celery with the Flask app instance
celery = make_celery(app)

# Import the blueprints
from train import train_bp
from predict import predict_bp
from download import download_bp
from metadata import metadata_bp
from job_status import job_status_bp
from health import health_bp  # Import the health blueprint

# Register the blueprints
app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')
app.register_blueprint(metadata_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/api')
app.register_blueprint(job_status_bp, url_prefix='/api')


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Bellmanbot Flask server!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
