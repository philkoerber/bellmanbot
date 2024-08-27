from flask import Blueprint, jsonify, request
from celery import current_app as celery

job_status_bp = Blueprint('job_status', __name__)

@job_status_bp.route('/job_status', methods=['GET'])
def job_status():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({"message": "Job ID parameter is missing."}), 400

    task = celery.AsyncResult(job_id)
    response = {
        'job_id': job_id,
        'status': task.status,
        'result': task.result if task.status == 'SUCCESS' else None
    }

    return jsonify(response), 200