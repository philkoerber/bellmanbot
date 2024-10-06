from flask import Blueprint, jsonify, request
from celery import current_app as celery
import os
import pandas as pd
import json
from datetime import datetime

train_bp = Blueprint('train', __name__)


@train_bp.route('/train', methods=['POST'])
def train():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"message": "Symbol parameter is missing."}), 400

    # Sanitize the symbol
    

    # Call the Celery task
    task = celery.send_task('train_model', args=[symbol])

    return jsonify({"message": f"Training started for symbol '{symbol}'", "job_id": task.id}), 202
