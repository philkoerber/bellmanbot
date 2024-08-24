from flask import Blueprint, jsonify, request
import os
import glob
from datetime import datetime

metadata_bp = Blueprint('metadata', __name__)

DATA_FOLDER = 'data'
MODELS_FOLDER = 'models'

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

@metadata_bp.route('/metadata', methods=['GET'])
def get_metadata():
    symbol = request.args.get('symbol', 'AAPL')
    safe_symbol = symbol.replace('/', '_')
    
    # Get data file metadata
    data_file_path = os.path.join(DATA_FOLDER, f'{safe_symbol}.csv')
    data_file_metadata = get_file_metadata(data_file_path)
    
    # Check if model exists for the symbol and get its metadata
    model_files = glob.glob(os.path.join(MODELS_FOLDER, f'{safe_symbol}_*.h5'))
    model_metadata = {}
    
    if model_files:
        for model_file in model_files:
            model_name = os.path.basename(model_file).split('.')[0]
            model_metadata[model_name] = get_file_metadata(model_file)
    else:
        model_metadata = None

    # Compile the metadata
    metadata = {
        'symbol': symbol,
        'data_file': data_file_metadata,
        'models': model_metadata
    }

    return jsonify(metadata)
