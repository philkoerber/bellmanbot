from flask import Blueprint, jsonify, request
import json
import os

# Create a Blueprint for predict
predict_bp = Blueprint('predict', __name__)

# Load symbols from symbols.json
def load_symbols():
    with open(os.path.join(os.path.dirname(__file__), 'symbols.json'), 'r') as f:
        return json.load(f)

# Define a route for /predict
@predict_bp.route('/predict', methods=['GET'])
def predict():
    # Get the 'symbol' parameter from the query string (metatraderName)
    metatrader_name = request.args.get('symbol')  # The request uses 'symbol' for metatraderName
    
    # Load symbols from the JSON file
    symbols = load_symbols()

    # Find the corresponding entry based on metatraderName
    symbol_info = next((s for s in symbols if s['metatraderName'] == metatrader_name), None)
    
    if symbol_info:
        # If found, retrieve the 'symbol' corresponding to the metatraderName
        symbol = symbol_info['symbol']
        return jsonify({"metatraderName": metatrader_name, "symbol": symbol})
    else:
        return jsonify({"message": "Symbol not found in the symbols.json"}), 404
