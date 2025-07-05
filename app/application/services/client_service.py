from typing import Optional
from app.application.dtos.client_dto import ClientDTO
from app.infrastructure.models.client import Client
from app.infrastructure.repositories.client_repository import ClientRepository  # or a defined interface

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repo = repository

    def create_client(self, dto: ClientDTO) -> Client:
        client = Client(name=dto.name, email=dto.email, phone=dto.phone)
        return self.repo.save(client)

    def get_clients(self) -> list[Client]:
        return self.repo.get_all()

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.repo.get_by_id(client_id)

    def update_client(self, client_id: int, dto: ClientDTO) -> Optional[Client]:
        client = self.repo.get_by_id(client_id)
        if client:
            client.name = dto.name
            client.email = dto.email
            client.phone = dto.phone
            return self.repo.update(client)
        return None

    def delete_client(self, client_id: int) -> bool:
        client = self.repo.get_by_id(client_id)
        if client:
            self.repo.delete(client)
            return True
        return False
