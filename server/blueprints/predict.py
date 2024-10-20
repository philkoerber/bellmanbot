from flask import Blueprint, jsonify, request
import json
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# Create a Blueprint for predict
predict_bp = Blueprint('predict', __name__)

# Configuration Constants
MODELS_FOLDER = 'models'

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

        symbol = symbol_info.get('symbol')
        safe_symbol = symbol.replace('/', '_')

        # Force Flask to parse the request body as JSON
        try:
            data = request.get_json(force=True)
        except Exception as e:
            print(f"JSON decode error: {e}")
            return jsonify({"message": f"Invalid JSON data in request body: {e}"}), 400

        # Access the chart data from the JSON
        chart_data = data.get('data', [])
        if not chart_data or len(chart_data) < 5:
            return jsonify({"message": "Insufficient chart data provided"}), 400

        # Convert chart data to DataFrame
        df = pd.DataFrame(chart_data)
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y.%m.%d %H:%M:%S')

        # Ensure data is sorted by datetime in ascending order
        df.sort_values('datetime', inplace=True)

        # Load the model and scalers
        model_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}.keras')
        scaler_X_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_X.pkl')
        scaler_y_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_y.pkl')

        if not os.path.exists(model_path):
            return jsonify({"message": f"Model for symbol '{symbol}' not found"}), 500
        if not os.path.exists(scaler_X_path) or not os.path.exists(scaler_y_path):
            return jsonify({"message": f"Scalers for symbol '{symbol}' not found"}), 500

        # Load the model and scalers
        model = tf.keras.models.load_model(model_path)
        scaler_X = pd.read_pickle(scaler_X_path)
        scaler_y = pd.read_pickle(scaler_y_path)

        # Prepare the input features
        # Ensure 'close' is included in features
        X = df[['open', 'high', 'low', 'close', 'volume']].values

        # Scale the input features
        X_scaled = scaler_X.transform(X)

        # Define the number of time steps (should match the model's input shape)
        time_steps = 5

        # Ensure we have enough data to create at least one sequence
        if len(X_scaled) < time_steps:
            return jsonify({"message": "Not enough data to create input sequences"}), 400

        # Prepare the input sequence
        input_seq = X_scaled[-time_steps:].reshape(1, time_steps, X_scaled.shape[1])

        # Predict the next 10 minutes iteratively
        predictions = []
        last_datetime = df['datetime'].iloc[-1]
        for i in range(10):
            # Predict the next value
            y_pred_scaled = model.predict(input_seq)

            # Inverse transform the predicted value
            y_pred = scaler_y.inverse_transform(y_pred_scaled)[0][0]

            # Append the prediction
            prediction_time = last_datetime + pd.Timedelta(minutes=i + 1)
            predictions.append({
                'predicted_close': float(y_pred),  # Convert to standard float
                'datetime': prediction_time
            })

            # Prepare the next input sequence
            # Create a new input by appending the predicted value
            # We'll update the 'close' value in the last row with the predicted value

            new_row = input_seq[0, -1, :].copy()
            # Update 'close' (assuming it's at index 3 in the features)
            y_pred_scaled = scaler_y.transform([[y_pred]])[0][0]
            new_row[3] = y_pred_scaled  # Update 'close' in the scaled input

            # Optionally update other features if needed (e.g., 'open', 'high', 'low', 'volume')
            # For simplicity, we'll keep them the same

            # Append the new row to the input sequence
            input_seq = np.append(input_seq[:, 1:, :], [[new_row]], axis=1)

        # Format the predictions for response
        predictions_formatted = []
        for pred in predictions:
            predictions_formatted.append({
                'datetime': pred['datetime'].strftime('%Y.%m.%d %H:%M:%S'),
                'predicted_close': pred['predicted_close']  # Already a standard float
            })

        # Construct the response
        response_data = {
            "symbol": symbol,
            "predictions": predictions_formatted
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception occurred: {e}")
        return jsonify({"message": str(e)}), 500
