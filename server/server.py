from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import time
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Import the blueprints
from train import train_bp
from predict import predict_bp
from download import download_bp
from metadata import metadata_bp


# Register the blueprints
app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')
app.register_blueprint(metadata_bp, url_prefix='/api')

# Store the start time of the server
start_time = time.time()

# Health status endpoint with server metrics
@app.route('/api/health_status', methods=['GET'])
def health_status():
    try:
        # Calculate server uptime
        uptime = time.time() - start_time

        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get memory usage
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        # Get disk usage
        disk_usage = psutil.disk_usage('/').percent

        # Get the number of active connections
        active_connections = len(psutil.net_connections())

        # Create the response with metrics
        message = (
            f"Server is running fine. Uptime: {uptime:.2f} seconds, "
            f"CPU Usage: {cpu_usage}% , Memory Usage: {memory_usage}%, "
            f"Disk Usage: {disk_usage}%, Active Connections: {active_connections}, "
            f"Process ID: {os.getpid()}."
        )

        health_metrics = {
            "status": "healthy",
            "message": message
        }

        return jsonify(health_metrics), 200

    except Exception as e:
        # If there's an issue, return an error message
        return jsonify({"status": "unhealthy", "message": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask server!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
