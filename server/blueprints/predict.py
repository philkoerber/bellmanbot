from flask import Blueprint, jsonify

# Create a Blueprint for predict
predict_bp = Blueprint('predict', __name__)

# Define a route for /predict
@predict_bp.route('/predict', methods=['GET'])
def predict():
    print("Received a call to /predict")
    return jsonify({"message": "hello from the bellman"})