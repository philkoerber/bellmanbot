from flask import Blueprint, jsonify, request
from celery import current_app as celery
import os

download_bp = Blueprint('download', __name__)

# Configuration
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY') or '83a3ab2d88ff4292a6b446d30b5d27bc'
DATA_FOLDER = 'data'

# Ensure the data directory exists
os.makedirs(DATA_FOLDER, exist_ok=True)

@download_bp.route('/download', methods=['POST'])
def download_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"message": "Symbol parameter is missing."}), 400

    # Call the Celery task
    task = celery.send_task('tasks.download_data', args=[symbol])

    return jsonify({"message": f"Download started for symbol '{symbol}'", "job_id": task.id}), 202