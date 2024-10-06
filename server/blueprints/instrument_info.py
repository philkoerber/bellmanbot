from flask import Blueprint, jsonify, request
import os
import json
import pandas as pd

# Create a Blueprint for instrument_info
instrument_info_bp = Blueprint('instrument_info', __name__)

# Define a route for /instrument_info
@instrument_info_bp.route('/instrument_info', methods=['POST'])
def instrument_info():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({"message": "Symbol parameter is missing."}), 400


    safe_symbol = symbol.replace('/', '_')

    # File paths
    csv_file_path = f'./data/{safe_symbol}.csv'
    log_file_path = f'./models/results/{safe_symbol}_log.json'

    
    # Check if CSV file exists and get its details
    if os.path.exists(csv_file_path):
        # Read CSV and count data points (rows)
        try:
            df = pd.read_csv(csv_file_path)
            data_points_count = len(df)
        except Exception as e:
            return jsonify({"message": f"Error reading CSV file: {str(e)}"}), 500
    else:
        return jsonify({"message": "CSV file for this symbol does not exist."})

    # Check if log file exists and get its contents
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r') as log_file:
                training_results = json.load(log_file)
        except Exception as e:
            return jsonify({"message": f"Error reading log file: {str(e)}"}), 500
    else:
        return jsonify({"message": "Log file for this symbol does not exist."})

    # Return both the CSV data points count and training results
    return jsonify({
        "data_points": data_points_count,
        "training_results": training_results
    }), 200
