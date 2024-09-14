from flask import Flask, jsonify
from flask_cors import CORS
from celery_config import make_celery
from blueprints import train_bp, predict_bp, download_bp, metadata_bp, job_status_bp, health_bp

app = Flask(__name__)
CORS(app)

celery = make_celery(app)

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