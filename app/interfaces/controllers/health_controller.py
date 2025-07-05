from flask import Blueprint, jsonify, Response

health_bp: Blueprint = Blueprint("health", __name__, url_prefix="/health")

@health_bp.route("/", strict_slashes=False)
def health_check() -> Response:
    return jsonify({"status": "healthy"})
