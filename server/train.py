from flask import Blueprint, jsonify, request
import os
import pandas as pd
import tensorflow as tf
import json
from datetime import datetime

train_bp = Blueprint('train', __name__)

MODEL_FOLDER = 'models'
DATA_FOLDER = 'data'
RESULTS_FOLDER = os.path.join(MODEL_FOLDER, 'results')

# Ensure the models and results directories exist
os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Define a simple RNN model with metrics
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(50, activation='relu', input_shape=(1, 4)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

@train_bp.route('/train', methods=['POST'])
def train():
    try:
        # Retrieve the symbol from the request parameters
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({"message": "Symbol parameter is missing."}), 400

        # Sanitize the symbol by replacing slashes with underscores
        sanitized_symbol = symbol.replace('/', '_')
        data_file = os.path.join(DATA_FOLDER, f'{sanitized_symbol}.csv')

        # Check if data file exists
        if not os.path.exists(data_file):
            return jsonify({"message": f"Data file for symbol '{symbol}' not found. Please upload the data first."}), 404

        # Load data from the CSV file
        df = pd.read_csv(data_file)

        # Prepare data for training
        X = df[['open', 'high', 'low', 'volume']].values  # Using 'open', 'high', 'low', and 'volume' as features
        y = df['close'].shift(-1).fillna(df['close']).values  # Predicting the next close (shifted by one time step)

        # Reshape the data for the RNN model
        X = X.reshape((X.shape[0], 1, X.shape[1]))  # Reshape for RNN input, with sequence length 1
        y = y.reshape((y.shape[0], 1))  # Reshape target variable

        # Create and train the model
        model = create_model()

        # Split data into training and validation sets
        train_size = int(len(X) * 0.8)
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]

        history = model.fit(
            X_train, y_train,
            epochs=5,
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=2
        )

        # Save the model in the .keras format in the models subfolder
        model_path = os.path.join(MODEL_FOLDER, f'{sanitized_symbol}.keras')
        model.save(model_path)

        # Prepare training results
        results = {
            "loss": history.history['loss'][-1],  # Latest loss value
            "accuracy": history.history.get('accuracy', [None])[-1],  # Accuracy, default to None
            "val_loss": history.history.get('val_loss', [None])[-1],  # Validation loss, default to None
            "val_accuracy": history.history.get('val_accuracy', [None])[-1]  # Validation accuracy, default to None
        }

        # Save results to JSON
        results_path = os.path.join(RESULTS_FOLDER, f'{sanitized_symbol}.json')
        with open(results_path, 'w') as f:
            json.dump(results, f)

        return jsonify({"message": f"Training completed and model for symbol '{symbol}' saved!"}), 200

    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        return jsonify({"message": "An internal error occurred. Please try again later."}), 500
