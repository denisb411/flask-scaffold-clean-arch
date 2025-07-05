from app.infrastructure.models.client import Client
from app.config import db

class ClientRepository:
    def get_all(self) -> list[Client]:
        return db.session.query(Client).all()

    def get_by_id(self, client_id: int) -> Client | None:
        return db.session.get(Client, client_id)

    def save(self, client: Client) -> Client:
        db.session.add(client)
        db.session.commit()
        return client

    def update(self, client: Client) -> Client:
        db.session.commit()
        return client

    def delete(self, client: Client) -> None:
        db.session.delete(client)
        db.session.commit()
