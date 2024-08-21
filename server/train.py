from flask import Blueprint, jsonify, request
import os
import pandas as pd
import tensorflow as tf
import numpy as np

train_bp = Blueprint('train', __name__)

MODEL_FOLDER = 'models'
DATA_FOLDER = 'data'

# Ensure the models directory exists
if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)

# Define a simple RNN model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(50, activation='relu', input_shape=(1, 2)),  # Input shape adjusted for bid and ask
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

@train_bp.route('/train', methods=['POST'])
def train():
    # Retrieve the symbol from the request parameters
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"message": "Symbol parameter is missing."})

    # Sanitize the symbol by replacing slashes with underscores
    sanitized_symbol = symbol.replace('/', '_')
    data_file = os.path.join(DATA_FOLDER, f'{sanitized_symbol}.csv')

    # Check if data file exists
    if not os.path.exists(data_file):
        return jsonify({"message": f"Data file for symbol '{symbol}' not found. Please upload the data first."})

    # Load data from the CSV file
    df = pd.read_csv(data_file)

    # Prepare data for training
    X = df[['bid', 'ask']].values  # Using both 'bid' and 'ask' as features
    y = df['bid'].shift(-1).fillna(df['bid']).values  # Predicting the next bid (shifted by one time step)
    
    # Reshape the data for the RNN model
    X = X.reshape((X.shape[0], 1, X.shape[1]))  # Reshape for RNN input, with sequence length 1
    y = y.reshape((y.shape[0], 1))  # Reshape target variable

    # Create and train the model
    model = create_model()
    model.fit(X, y, epochs=1, batch_size=32, verbose=2)  # Train for 1 epoch for simplicity

    # Save the model in the .keras format in the models subfolder
    model_path = os.path.join(MODEL_FOLDER, f'{sanitized_symbol}_rnn_model.keras')
    model.save(model_path)

    return jsonify({"message": f"Training completed and model for symbol '{symbol}' saved!"})
