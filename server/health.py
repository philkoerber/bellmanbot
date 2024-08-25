from flask import Blueprint, jsonify
import psutil
import time
import os

health_bp = Blueprint('health', __name__)

# Store the start time of the server
start_time = time.time()

@health_bp.route('/health_status', methods=['GET'])
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
