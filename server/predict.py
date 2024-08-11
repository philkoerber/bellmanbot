from flask import Blueprint, jsonify

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    # Dummy response
    return jsonify({"message": "Prediction initiated!"})
