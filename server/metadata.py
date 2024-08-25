from flask import Blueprint, jsonify, request
import os
import json
from datetime import datetime

metadata_bp = Blueprint('metadata', __name__)

DATA_FOLDER = 'data'
MODELS_FOLDER = 'models'
RESULTS_FOLDER = os.path.join(MODELS_FOLDER, 'results')

def get_file_metadata(file_path):
    """ Helper function to get metadata about a file """
    if not os.path.exists(file_path):
        return None

    file_stats = os.stat(file_path)
    file_size = file_stats.st_size
    last_modified = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'size': file_size,
        'last_modified': last_modified
    }

def get_results_metadata(symbol):
    """ Helper function to get the results metadata for a symbol """
    results_file_path = os.path.join(RESULTS_FOLDER, f'{symbol}.json')
    if os.path.exists(results_file_path):
        with open(results_file_path, 'r') as f:
            return json.load(f)
    return None

@metadata_bp.route('/metadata', methods=['GET'])
def get_metadata():
    symbol = request.args.get('symbol', 'AAPL')
    safe_symbol = symbol.replace('/', '_')
    
    # Get data file metadata
    data_file_path = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')
    data_file_metadata = get_file_metadata(data_file_path)
    
    # Get results metadata
    results_metadata = get_results_metadata(safe_symbol)

    # Compile the metadata
    metadata = {
        'symbol': symbol,
        'data_file': data_file_metadata,
        'results': results_metadata
    }

    return jsonify(metadata)