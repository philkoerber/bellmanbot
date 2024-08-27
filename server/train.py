from flask import Blueprint, jsonify, request
from celery import current_app as celery
import os
import pandas as pd
import json
from datetime import datetime
from tasks import train_model  # Import the Celery task

train_bp = Blueprint('train', __name__)

MODEL_FOLDER = 'models'
DATA_FOLDER = 'data'
RESULTS_FOLDER = os.path.join(MODEL_FOLDER, 'results')

# Ensure the models and results directories exist
os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@train_bp.route('/train', methods=['POST'])
def train():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"message": "Symbol parameter is missing."}), 400

    # Sanitize the symbol
    sanitized_symbol = symbol.replace('/', '_')

    # Call the Celery task
    task = train_model.delay(sanitized_symbol)

    return jsonify({"message": f"Training started for symbol '{symbol}'", "job_id": task.id}), 202
