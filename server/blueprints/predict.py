from flask import Blueprint, jsonify, request
import json
import os
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

# Create a Blueprint for predict
predict_bp = Blueprint('predict', __name__)

MODELS_FOLDER = 'models'
TIME_STEPS = 5  # This should match the time steps used during training

# Load symbols from symbols.json
def load_symbols():
    with open(os.path.join(os.path.dirname(__file__), 'symbols.json'), 'r') as f:
        return json.load(f)

# Helper function to load the model
def load_model(symbol):
    safe_symbol = symbol.replace('/', '_')
    model_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}.keras')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file for symbol '{symbol}' not found.")
    return tf.keras.models.load_model(model_path)

# Helper function to load scalers
def load_scalers(symbol):
    safe_symbol = symbol.replace('/', '_')
    scaler_X_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_X.pkl')
    scaler_y_path = os.path.join(MODELS_FOLDER, f'{safe_symbol}_scaler_y.pkl')
    if not os.path.exists(scaler_X_path) or not os.path.exists(scaler_y_path):
        raise FileNotFoundError(f"Scaler files for symbol '{safe_symbol}' not found.")
    scaler_X = pd.read_pickle(scaler_X_path)
    scaler_y = pd.read_pickle(scaler_y_path)
    return scaler_X, scaler_y

# Define a route for /predict
@predict_bp.route('/predict', methods=['GET'])
def predict():
    # Get the 'symbol' parameter from the query string (metatraderName)
    metatrader_name = request.args.get('symbol')  # The request uses 'symbol' for metatraderName
    
    # Load symbols from the JSON file
    symbols = load_symbols()

    # Find the corresponding entry based on metatraderName
    symbol_info = next((s for s in symbols if s['metatraderName'] == metatrader_name), None)


    
    
    if not symbol_info:
        return jsonify({"message": "Symbol not found in the symbols.json"}), 404

    # If found, retrieve the 'symbol' corresponding to the metatraderName
    symbol = symbol_info['symbol']

    try:
        # Load model and scalers
        model = load_model(symbol)
        scaler_X, scaler_y = load_scalers(symbol)

        # Simulating input data (replace with real data coming from MetaTrader)
        # The input should have the same structure as during training
        input_data = np.array([
            [1.2345, 1.2356, 1.2334, 1000],  # Example data: [open, high, low, volume]
            [1.2356, 1.2367, 1.2345, 1200],
            [1.2367, 1.2378, 1.2356, 1500],
            [1.2378, 1.2389, 1.2367, 1300],
            [1.2389, 1.2390, 1.2378, 1400]
        ])

        # Ensure the input is scaled correctly
        input_scaled = scaler_X.transform(input_data)

        # Reshape input to match model's expected input shape
        input_scaled = np.expand_dims(input_scaled, axis=0)  # Shape should be (1, TIME_STEPS, features)

        # Make the prediction
        prediction_scaled = model.predict(input_scaled)

        # Inverse transform the prediction to get the actual price
        prediction = scaler_y.inverse_transform(prediction_scaled)

        return jsonify({"metatraderName": metatrader_name, "symbol": symbol, "prediction": float(prediction[0][0])})

    except Exception as e:
        return jsonify({"message": str(e)}), 500
