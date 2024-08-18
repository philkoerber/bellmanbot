from flask import Blueprint, jsonify
import os
import pandas as pd
import tensorflow as tf
import numpy as np

train_bp = Blueprint('train', __name__)

DATA_FILE = 'historical_data.csv'
MODEL_FOLDER = 'models'

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
    # Check if data exists
    if not os.path.exists(DATA_FILE):
        return jsonify({"message": "Data file not found. Please download the data first."})

    # Load data from the CSV file
    df = pd.read_csv(DATA_FILE)

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
    model_path = os.path.join(MODEL_FOLDER, 'rnn_model.keras')
    model.save(model_path)

    return jsonify({"message": "Training completed and model saved!"})
