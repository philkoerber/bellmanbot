from flask import Blueprint, jsonify, request
import json
import os

# Create a Blueprint for predict
predict_bp = Blueprint('predict', __name__)

# Load symbols from symbols.json
def load_symbols():
    symbols_path = os.path.join(os.path.dirname(__file__), 'symbols.json')
    with open(symbols_path, 'r') as f:
        return json.load(f)

# Define a route for /predict
@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the 'symbol' parameter from the query string
        metatrader_name = request.args.get('symbol')

        if not metatrader_name:
            return jsonify({"message": "Symbol parameter is missing in the URL"}), 400

        # Load symbols from the JSON file
        symbols = load_symbols()

        # Find the corresponding entry based on metatraderName
        symbol_info = next((s for s in symbols if s.get('metatraderName') == metatrader_name), None)

        if not symbol_info:
            return jsonify({"message": "Symbol not found in symbols.json"}), 404

        # Force Flask to parse the request body as JSON
        try:
            data = request.get_json(force=True)
        except Exception as e:
            print(f"JSON decode error: {e}")
            return jsonify({"message": f"Invalid JSON data in request body: {e}"}), 400

        # Access the data from the JSON
        message = data.get('message', '')
        chart_data = data.get('data', {})

        # Do something with the message and chart data
        print(f"Received message: {message}")
        print(f"Received chart data: {chart_data}")

        # Construct the response
        response_data = {
            "symbol": symbol_info.get('symbol'),
            "received_message": message,
            "received_chart_data": chart_data
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception occurred: {e}")
        return jsonify({"message": str(e)}), 500
