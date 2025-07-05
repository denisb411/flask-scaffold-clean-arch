from flask import Blueprint, request, jsonify, Response
from flasgger import swag_from  # type: ignore[import]
from typing import Callable
from app.application.dtos.client_dto import ClientDTO
from app.utils.logging import log_request
from app.application.exceptions import NotFoundError, BadRequestError
from app.application.services.protocols import ClientServiceProtocol
from app.utils.json_body import get_valid_json_body


def create_client_blueprint(client_service: ClientServiceProtocol) -> Blueprint:
    bp = Blueprint("clients", __name__)

    @bp.route("/", methods=["GET"])
    @log_request
    @swag_from(
        {
            "responses": {
                200: {
                    "description": "List of clients",
                    "examples": {
                        "application/json": [
                            {
                                "id": 1,
                                "name": "John",
                                "email": "john@example.com",
                                "phone": "123456",
                            }
                        ]
                    },
                }
            }
        }
    )
    def list_clients() -> Response:
        clients = client_service.get_clients()
        return jsonify(
            [
                {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone}
                for c in clients
            ]
        )

    @bp.route("/<int:client_id>", methods=["GET"])
    @log_request
    @swag_from(
        {
            "responses": {
                200: {
                    "description": "Client details",
                    "examples": {
                        "application/json": {
                            "id": 1,
                            "name": "John",
                            "email": "john@example.com",
                            "phone": "123456",
                        }
                    },
                },
                404: {"description": "Client not found"},
            },
            "parameters": [
                {"name": "client_id", "in": "path", "type": "integer", "required": True}
            ],
        }
    )
    def get_client(client_id: int) -> Response:
        client = client_service.get_client_by_id(client_id)
        if not client:
            raise NotFoundError("Client not found")
        return jsonify(
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
            }
        )

    @bp.route("/", methods=["POST"])
    @log_request
    @swag_from(
        {
            "responses": {
                201: {"description": "Created"},
                400: {"description": "Bad Request"},
            },
            "parameters": [
                {"name": "body", "in": "body", "schema": ClientDTO.model_json_schema()}
            ],
        }
    )
    def create_client() -> tuple[Response, int]:
        try:
            data = ClientDTO.from_request(get_valid_json_body())
        except Exception as e:
            raise BadRequestError(str(e))
        client = client_service.create_client(data)
        return (
            jsonify(
                {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone,
                }
            ),
            201,
        )

    @bp.route("/<int:client_id>", methods=["PUT"])
    @log_request
    @swag_from(
        {
            "responses": {
                200: {"description": "Updated successfully"},
                400: {"description": "Bad request"},
                404: {"description": "Client not found"},
            },
            "parameters": [
                {
                    "name": "client_id",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                },
                {"name": "body", "in": "body", "schema": ClientDTO.model_json_schema()},
            ],
        }
    )
    def update_client(client_id: int) -> Response:
        try:
            data = ClientDTO.from_request(get_valid_json_body())
        except Exception as e:
            raise BadRequestError(str(e))
        client = client_service.update_client(client_id, data)
        if not client:
            raise NotFoundError("Client not found")
        return jsonify(
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
            }
        )

    @bp.route("/<int:client_id>", methods=["DELETE"])
    @log_request
    @swag_from(
        {
            "responses": {
                200: {"description": "Client deleted"},
                404: {"description": "Client not found"},
            },
            "parameters": [
                {"name": "client_id", "in": "path", "type": "integer", "required": True}
            ],
        }
    )
    def delete_client(client_id: int) -> Response:
        success = client_service.delete_client(client_id)
        if not success:
            raise NotFoundError("Client not found")
        return jsonify({"status": "deleted"})

    return bp
