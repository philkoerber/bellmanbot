from flask import Blueprint, jsonify
import tensorflow as tf
import numpy as np

train_bp = Blueprint('train', __name__)

# Define a simple RNN model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(50, activation='relu', input_shape=(10, 1)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

@train_bp.route('/train', methods=['POST'])
def train():
    # Dummy data for training
    x_train = np.random.random((100, 10, 1))
    y_train = np.random.random((100, 1))

    # Create and train the model
    model = create_model()
    model.fit(x_train, y_train, epochs=1)  # Train for 1 epoch for simplicity

    # Save the model in the new .keras format
    model.save('rnn_model.keras')

    return jsonify({"message": "Training completed and model saved!"})
