from flask import Blueprint, jsonify
import tensorflow as tf
import numpy as np

predict_bp = Blueprint('predict', __name__)

# Load the model in .keras format
def load_model():
    return tf.keras.models.load_model('rnn_model.keras')

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Load the model
        model = load_model()

        # Dummy data for prediction
        x_test = np.random.random((1, 10, 1))

        # Make predictions
        predictions = model.predict(x_test)

        return jsonify({"message": predictions.tolist()})
    except Exception as e:
        return jsonify({"message": "Prediction failed!", "error": str(e)}), 500
