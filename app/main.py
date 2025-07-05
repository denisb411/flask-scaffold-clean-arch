from flask import Flask, jsonify, Response
from flasgger import Swagger # type: ignore[import]
from app.config import db, DATABASE_URL
from app.interfaces.controllers.client_controller import create_client_blueprint
from app.interfaces.controllers.health_controller import health_bp
from app.containers import Container
from app.application.exceptions import AppError


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    Swagger(app)

    container = Container()
    container.config.from_dict({"DATABASE_URL": DATABASE_URL})
    db.init_app(app)

    app.register_blueprint(
        create_client_blueprint(container.client_service()),
        url_prefix="/api/v1/clients",
    )
    app.register_blueprint(health_bp)

    # Centralized error handling
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError) -> Response:
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    # ensure the Python modules defining your models are imported
    from app.infrastructure.models.client import Client
    from app.infrastructure.models.base_model import Base as SA_Base

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
